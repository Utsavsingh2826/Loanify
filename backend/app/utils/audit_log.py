"""Audit logging utilities."""
from datetime import datetime
from typing import Dict, Any, Optional
from app.utils.database import get_mongo_db
from app.utils.logger import get_logger
import uuid

logger = get_logger(__name__)


class AuditLogger:
    """Audit logger for compliance."""
    
    def __init__(self):
        """Initialize audit logger."""
        self.collection_name = "audit_logs"
    
    def log_event(
        self,
        event_type: str,
        user_id: Optional[str],
        action: str,
        details: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> str:
        """Log an audit event."""
        try:
            db = get_mongo_db()
            collection = db[self.collection_name]
            
            audit_entry = {
                "_id": str(uuid.uuid4()),
                "event_type": event_type,
                "user_id": user_id,
                "action": action,
                "details": details,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "timestamp": datetime.utcnow(),
            }
            
            collection.insert_one(audit_entry)
            
            logger.info(
                "audit_event_logged",
                event_type=event_type,
                user_id=user_id,
                action=action
            )
            
            return audit_entry["_id"]
            
        except Exception as e:
            logger.error("audit_log_error", error=str(e))
            return None
    
    def get_user_audit_trail(
        self,
        user_id: str,
        limit: int = 100
    ) -> list:
        """Get audit trail for a user."""
        try:
            db = get_mongo_db()
            collection = db[self.collection_name]
            
            cursor = collection.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit)
            
            return list(cursor)
            
        except Exception as e:
            logger.error("audit_trail_error", error=str(e))
            return []
    
    def get_audit_logs(
        self,
        event_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 1000
    ) -> list:
        """Get audit logs with filters."""
        try:
            db = get_mongo_db()
            collection = db[self.collection_name]
            
            query = {}
            if event_type:
                query["event_type"] = event_type
            if start_date or end_date:
                query["timestamp"] = {}
                if start_date:
                    query["timestamp"]["$gte"] = start_date
                if end_date:
                    query["timestamp"]["$lte"] = end_date
            
            cursor = collection.find(query).sort("timestamp", -1).limit(limit)
            return list(cursor)
            
        except Exception as e:
            logger.error("get_audit_logs_error", error=str(e))
            return []


# Global audit logger instance
audit_logger = AuditLogger()


