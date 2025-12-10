"""Notification service for email and SMS (Mock implementation)."""
from typing import Dict, Any, Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    """Mock service for notifications."""
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachment_path: Optional[str] = None
    ) -> bool:
        """
        Send email (mock).
        
        In production, this would integrate with SendGrid/Mailgun.
        """
        try:
            # Mock email sending
            logger.info(
                "email_sent",
                to=to_email,
                subject=subject,
                has_attachment=attachment_path is not None
            )
            
            # Simulate success
            return True
            
        except Exception as e:
            logger.error("email_send_error", error=str(e))
            return False
    
    async def send_sms(
        self,
        phone_number: str,
        message: str
    ) -> bool:
        """
        Send SMS (mock).
        
        In production, this would integrate with Twilio/AWS SNS.
        """
        try:
            # Mock SMS sending
            logger.info(
                "sms_sent",
                to=phone_number,
                message_length=len(message)
            )
            
            # Simulate success
            return True
            
        except Exception as e:
            logger.error("sms_send_error", error=str(e))
            return False
    
    async def send_whatsapp_message(
        self,
        phone_number: str,
        message: str
    ) -> bool:
        """
        Send WhatsApp message (mock).
        
        In production, this would integrate with WhatsApp Business API.
        """
        try:
            # Mock WhatsApp sending
            logger.info(
                "whatsapp_sent",
                to=phone_number,
                message_length=len(message)
            )
            
            # Simulate success
            return True
            
        except Exception as e:
            logger.error("whatsapp_send_error", error=str(e))
            return False
    
    async def send_application_status_update(
        self,
        user_contact: Dict[str, str],
        status: str,
        application_number: str
    ) -> bool:
        """Send application status update via preferred channel."""
        try:
            message = f"Your loan application {application_number} status: {status}"
            
            # Send via multiple channels
            if user_contact.get("email"):
                await self.send_email(
                    to_email=user_contact["email"],
                    subject=f"Loan Application Status Update - {application_number}",
                    body=message
                )
            
            if user_contact.get("phone"):
                await self.send_sms(
                    phone_number=user_contact["phone"],
                    message=message
                )
            
            return True
            
        except Exception as e:
            logger.error("status_update_error", error=str(e))
            return False


# Global notification service instance
notification_service = NotificationService()


