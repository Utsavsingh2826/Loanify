"""Document processing and management service."""
from typing import Dict, Any, Optional
import os
import uuid
from datetime import datetime
from app.config import settings
from app.utils.logger import get_logger
from app.services.ocr_service import ocr_service
from app.services.fraud_detection_service import fraud_detection_service

logger = get_logger(__name__)


class DocumentService:
    """Service for document processing."""
    
    def __init__(self):
        """Initialize document service."""
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_document(
        self,
        file_content: bytes,
        filename: str,
        document_type: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Save uploaded document."""
        try:
            # Generate unique filename
            file_ext = os.path.splitext(filename)[1]
            unique_filename = f"{user_id}_{document_type}_{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(self.upload_dir, unique_filename)
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            logger.info(
                "document_saved",
                filename=unique_filename,
                document_type=document_type,
                user_id=user_id
            )
            
            return {
                "success": True,
                "file_path": file_path,
                "filename": unique_filename,
                "document_type": document_type
            }
            
        except Exception as e:
            logger.error("document_save_error", error=str(e))
            return {"success": False, "error": str(e)}
    
    async def verify_document(
        self,
        document_id: str,
        document_type: str
    ) -> Dict[str, Any]:
        """Verify document authenticity and extract data."""
        try:
            # Mock document verification
            # In production, this would call OCR and validation services
            
            # Extract data using OCR
            extracted_data = await ocr_service.extract_document_data(
                document_id,
                document_type
            )
            
            # Check for fraud
            fraud_check = await fraud_detection_service.check_document(
                document_id,
                extracted_data
            )
            
            # Validate extracted data
            validation = self._validate_document_data(
                document_type,
                extracted_data
            )
            
            result = {
                "valid": validation["valid"] and not fraud_check["suspicious"],
                "document_type": document_type,
                "extracted_data": extracted_data,
                "confidence_score": extracted_data.get("confidence", 0),
                "fraud_flags": fraud_check.get("flags", []),
                "validation_errors": validation.get("errors", [])
            }
            
            logger.info(
                "document_verified",
                document_type=document_type,
                valid=result["valid"]
            )
            
            return result
            
        except Exception as e:
            logger.error("document_verification_error", error=str(e))
            return {
                "valid": False,
                "error": str(e)
            }
    
    def _validate_document_data(
        self,
        document_type: str,
        extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate extracted document data."""
        errors = []
        
        if document_type == "pan_card":
            pan = extracted_data.get("pan_number", "")
            if not self._validate_pan(pan):
                errors.append("Invalid PAN format")
            
            if not extracted_data.get("name"):
                errors.append("Name not found")
        
        elif document_type == "aadhaar_card":
            aadhaar = extracted_data.get("aadhaar_number", "")
            if not self._validate_aadhaar(aadhaar):
                errors.append("Invalid Aadhaar format")
        
        elif document_type == "bank_statement":
            if not extracted_data.get("account_number"):
                errors.append("Account number not found")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _validate_pan(self, pan: str) -> bool:
        """Validate PAN number format."""
        import re
        pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        return bool(re.match(pattern, pan))
    
    def _validate_aadhaar(self, aadhaar: str) -> bool:
        """Validate Aadhaar number format."""
        # Remove spaces
        aadhaar = aadhaar.replace(" ", "")
        return len(aadhaar) == 12 and aadhaar.isdigit()


# Global document service instance
document_service = DocumentService()


