"""Conversation data models."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.utils.database import Base


class ConversationStatus(str, enum.Enum):
    """Conversation status enum."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    TRANSFERRED = "transferred"


class MessageRole(str, enum.Enum):
    """Message role enum."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AgentType(str, enum.Enum):
    """Agent type enum."""
    MASTER = "master"
    ENGAGE = "engage"
    VERIFY = "verify"
    UNDERWRITE = "underwrite"
    SANCTION = "sanction"


class Conversation(Base):
    """Conversation model."""
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ConversationStatus), default=ConversationStatus.ACTIVE)
    current_agent = Column(Enum(AgentType), default=AgentType.MASTER)
    
    # Conversation metadata
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    message_count = Column(Integer, default=0)
    
    # State management
    conversation_state = Column(JSONB, default={})  # Store agent-specific state
    context = Column(JSONB, default={})  # Store conversation context
    
    # Sentiment tracking
    overall_sentiment = Column(String, nullable=True)
    sentiment_score = Column(String, nullable=True)


class Message(Base):
    """Message model."""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    
    # Agent information
    agent_type = Column(Enum(AgentType), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    message_metadata = Column(JSONB, default={})  # Store additional info like sentiment, etc.
    
    # Voice support
    audio_url = Column(String, nullable=True)
    is_voice_message = Column(String, default=False)

