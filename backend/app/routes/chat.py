"""Chat API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from app.utils.database import get_db, get_mongo_db
from app.utils.logger import get_logger
from app.models.user import User
from app.models.conversation import Conversation, Message, ConversationStatus, MessageRole, AgentType
from app.models.loan_application import LoanApplication, ApplicationStatus
from app.agents.master_agent import MasterAgent
from app.agents.engage_agent import EngageAgent
from app.agents.verify_agent import VerifyAgent
from app.agents.underwrite_agent import UnderwriteAgent
from app.agents.sanction_agent import SanctionAgent
from app.services.sentiment_service import sentiment_service
from app.utils.cache import cache

logger = get_logger(__name__)
router = APIRouter()


# Request/Response models
class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: str
    language: Optional[str] = "english"


class ChatMessageResponse(BaseModel):
    response: str
    conversation_id: str
    agent: str
    sentiment: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None


class ConversationHistory(BaseModel):
    conversation_id: str
    messages: List[Dict[str, Any]]
    status: str
    created_at: datetime


# Initialize agents
master_agent = MasterAgent()
engage_agent = EngageAgent()
verify_agent = VerifyAgent()
underwrite_agent = UnderwriteAgent()
sanction_agent = SanctionAgent()


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """Send a message and get response from appropriate agent."""
    try:
        # Get or create conversation
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id
            ).first()
            
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(
                id=uuid.uuid4(),
                user_id=request.user_id,
                status=ConversationStatus.ACTIVE,
                current_agent=AgentType.MASTER,
                conversation_state={},
                context={"preferred_language": request.language}
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            # Create loan application
            application = LoanApplication(
                id=uuid.uuid4(),
                application_number=f"APP{str(uuid.uuid4())[:8].upper()}",
                user_id=request.user_id,
                conversation_id=conversation.id,
                status=ApplicationStatus.INITIATED
            )
            db.add(application)
            db.commit()
        
        # Analyze sentiment
        sentiment_result = await sentiment_service.analyze_sentiment(request.message)
        
        # Save user message
        user_message = Message(
            id=uuid.uuid4(),
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.message,
            message_metadata={"sentiment": sentiment_result}
        )
        db.add(user_message)
        db.commit()
        
        # Get conversation history from MongoDB
        mongo_db = get_mongo_db()
        history_collection = mongo_db["conversation_history"]
        
        history_doc = history_collection.find_one({"conversation_id": str(conversation.id)})
        if history_doc:
            conversation_history = history_doc.get("messages", [])
        else:
            conversation_history = []
        
        # Add current message to history
        conversation_history.append({
            "role": "user",
            "content": request.message
        })
        
        # Determine which agent to use
        current_agent_type = conversation.current_agent
        context = conversation.conversation_state or {}
        context["conversation_id"] = str(conversation.id)
        context["application_number"] = db.query(LoanApplication).filter(
            LoanApplication.conversation_id == conversation.id
        ).first().application_number
        
        # Route to appropriate agent
        agent_map = {
            AgentType.MASTER: master_agent,
            AgentType.ENGAGE: engage_agent,
            AgentType.VERIFY: verify_agent,
            AgentType.UNDERWRITE: underwrite_agent,
            AgentType.SANCTION: sanction_agent
        }
        
        agent = agent_map.get(current_agent_type, master_agent)
        
        # Process message with agent
        agent_response = await agent.process(
            user_message=request.message,
            conversation_history=conversation_history,
            context=context
        )
        
        response_text = agent_response["response"]
        updated_context = agent_response.get("context", context)
        
        # Check if handoff is needed
        if agent_response.get("should_handoff"):
            next_agent = updated_context.get("next_agent")
            if next_agent:
                conversation.current_agent = AgentType[next_agent.upper()]
        
        # Update conversation
        conversation.conversation_state = updated_context
        conversation.last_message_at = datetime.utcnow()
        conversation.message_count += 1
        
        # Save assistant message
        assistant_message = Message(
            id=uuid.uuid4(),
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=response_text,
            agent_type=current_agent_type,
            message_metadata={}
        )
        db.add(assistant_message)
        db.commit()
        
        # Update MongoDB history
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        history_collection.update_one(
            {"conversation_id": str(conversation.id)},
            {"$set": {"messages": conversation_history, "updated_at": datetime.utcnow()}},
            upsert=True
        )
        
        # Cache session
        cache.set_session(str(conversation.id), updated_context)
        
        logger.info(
            "message_processed",
            conversation_id=str(conversation.id),
            agent=current_agent_type.value
        )
        
        return ChatMessageResponse(
            response=response_text,
            conversation_id=str(conversation.id),
            agent=current_agent_type.value,
            sentiment=sentiment_result,
            context=updated_context
        )
        
    except Exception as e:
        logger.error("chat_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{conversation_id}", response_model=ConversationHistory)
async def get_conversation_history(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get conversation history."""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get messages from MongoDB
        mongo_db = get_mongo_db()
        history_collection = mongo_db["conversation_history"]
        
        history_doc = history_collection.find_one({"conversation_id": conversation_id})
        messages = history_doc.get("messages", []) if history_doc else []
        
        return ConversationHistory(
            conversation_id=conversation_id,
            messages=messages,
            status=conversation.status.value,
            created_at=conversation.started_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_history_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/user/{user_id}")
async def get_user_conversations(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all conversations for a user."""
    try:
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.started_at.desc()).all()
        
        return {
            "user_id": user_id,
            "conversations": [
                {
                    "id": str(conv.id),
                    "status": conv.status.value,
                    "current_agent": conv.current_agent.value,
                    "started_at": conv.started_at.isoformat(),
                    "message_count": conv.message_count
                }
                for conv in conversations
            ]
        }
        
    except Exception as e:
        logger.error("get_conversations_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

