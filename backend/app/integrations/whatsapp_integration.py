"""WhatsApp Business API integration (Mock)."""
from typing import Dict, Any
from app.utils.logger import get_logger

logger = get_logger(__name__)


class WhatsAppIntegration:
    """Mock WhatsApp Business API service."""
    
    async def send_message(
        self,
        phone_number: str,
        message: str
    ) -> Dict[str, Any]:
        """Send WhatsApp message."""
        try:
            # Mock WhatsApp message sending
            logger.info(
                "whatsapp_message_sent",
                phone=phone_number,
                message_length=len(message)
            )
            
            return {
                "success": True,
                "message_id": f"wamid_{phone_number}_{hash(message)}",
                "status": "sent"
            }
            
        except Exception as e:
            logger.error("whatsapp_error", error=str(e))
            return {"success": False, "error": str(e)}
    
    async def send_template_message(
        self,
        phone_number: str,
        template_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send WhatsApp template message."""
        try:
            logger.info(
                "whatsapp_template_sent",
                phone=phone_number,
                template=template_name
            )
            
            return {
                "success": True,
                "message_id": f"wamid_template_{phone_number}",
                "status": "sent"
            }
            
        except Exception as e:
            logger.error("whatsapp_template_error", error=str(e))
            return {"success": False, "error": str(e)}


# Global WhatsApp integration instance
whatsapp_integration = WhatsAppIntegration()


