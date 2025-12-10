"""WebSocket endpoints for real-time chat."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import Dict, Set
import json
import uuid
from datetime import datetime

from app.utils.database import get_db
from app.utils.logger import get_logger
from app.models.conversation import Conversation, Message, MessageRole, AgentType, ConversationStatus
from app.agents.master_agent import MasterAgent
from app.agents.engage_agent import EngageAgent
from app.agents.verify_agent import VerifyAgent
from app.agents.underwrite_agent import UnderwriteAgent
from app.agents.sanction_agent import SanctionAgent

logger = get_logger(__name__)
router = APIRouter()


# Connection manager
class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Connect a new client."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info("websocket_connected", client_id=client_id)
    
    def disconnect(self, client_id: str):
        """Disconnect a client."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info("websocket_disconnected", client_id=client_id)
    
    async def send_message(self, client_id: str, message: dict):
        """Send message to specific client."""
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all clients."""
        for connection in self.active_connections.values():
            await connection.send_json(message)


manager = ConnectionManager()

# Initialize agents
master_agent = MasterAgent()
engage_agent = EngageAgent()
verify_agent = VerifyAgent()
underwrite_agent = UnderwriteAgent()
sanction_agent = SanctionAgent()


@router.websocket("/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat."""
    client_id = f"{user_id}_{uuid.uuid4()}"
    await manager.connect(websocket, client_id)
    
    # Send welcome message
    await manager.send_message(client_id, {
        "type": "system",
        "message": "Connected to LoaniFi AI Assistant",
        "timestamp": datetime.utcnow().isoformat()
    })
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Send typing indicator
            await manager.send_message(client_id, {
                "type": "typing",
                "agent": message_data.get("current_agent", "master")
            })
            
            # Process message (simplified version)
            response_text = f"Received: {message_data.get('message')}"
            
            # Send response
            await manager.send_message(client_id, {
                "type": "message",
                "content": response_text,
                "agent": message_data.get("current_agent", "master"),
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info("websocket_disconnect", client_id=client_id)
    except Exception as e:
        logger.error("websocket_error", error=str(e), client_id=client_id)
        manager.disconnect(client_id)


