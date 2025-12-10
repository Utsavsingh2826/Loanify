"""OCR service for document data extraction (Mock implementation)."""
from typing import Dict, Any
import random
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OCRService:
    """Mock service for OCR document extraction."""
    
    async def extract_document_data(
        self,
        document_id: str,
        document_type: str
    ) -> Dict[str, Any]:
        """
        Extract data from document using OCR (mock).
        
        In production, this would use Google Vision API, AWS Textract, or Tesseract.
        """
        try:
            # Mock extraction based on document type
            if document_type == "pan_card":
                return await self._extract_pan_card(document_id)
            elif document_type == "aadhaar_card":
                return await self._extract_aadhaar_card(document_id)
            elif document_type == "bank_statement":
                return await self._extract_bank_statement(document_id)
            elif document_type == "income_proof":
                return await self._extract_income_proof(document_id)
            else:
                return {
                    "document_type": document_type,
                    "confidence": random.uniform(0.7, 0.95)
                }
                
        except Exception as e:
            logger.error("ocr_extraction_error", error=str(e))
            return {
                "error": str(e),
                "confidence": 0
            }
    
    async def _extract_pan_card(self, document_id: str) -> Dict[str, Any]:
        """Extract PAN card data."""
        # Mock PAN card extraction
        data = {
            "document_type": "pan_card",
            "pan_number": "ABCDE1234F",
            "name": "RAJESH KUMAR SHARMA",
            "father_name": "RAMESH SHARMA",
            "date_of_birth": "15/08/1985",
            "confidence": random.uniform(0.85, 0.98)
        }
        
        logger.info("pan_card_extracted", pan=data["pan_number"])
        return data
    
    async def _extract_aadhaar_card(self, document_id: str) -> Dict[str, Any]:
        """Extract Aadhaar card data."""
        # Mock Aadhaar extraction
        data = {
            "document_type": "aadhaar_card",
            "aadhaar_number": "XXXX XXXX 5678",  # Masked for privacy
            "name": "Rajesh Kumar Sharma",
            "date_of_birth": "15/08/1985",
            "gender": "Male",
            "address": "123, MG Road, Bangalore, Karnataka - 560001",
            "confidence": random.uniform(0.85, 0.98)
        }
        
        logger.info("aadhaar_extracted")
        return data
    
    async def _extract_bank_statement(self, document_id: str) -> Dict[str, Any]:
        """Extract bank statement data."""
        # Mock bank statement extraction
        data = {
            "document_type": "bank_statement",
            "bank_name": "HDFC Bank",
            "account_number": "XXXX XXXX 4567",
            "account_holder_name": "RAJESH KUMAR SHARMA",
            "statement_period": "01/09/2024 to 30/11/2024",
            "average_monthly_balance": random.randint(50000, 200000),
            "monthly_credits": [
                random.randint(45000, 65000),
                random.randint(45000, 65000),
                random.randint(45000, 65000)
            ],
            "bounced_transactions": 0,
            "overdraft_usage": False,
            "confidence": random.uniform(0.75, 0.92)
        }
        
        logger.info("bank_statement_extracted", bank=data["bank_name"])
        return data
    
    async def _extract_income_proof(self, document_id: str) -> Dict[str, Any]:
        """Extract income proof data."""
        # Mock income proof extraction
        data = {
            "document_type": "income_proof",
            "document_subtype": "salary_slip",
            "employee_name": "RAJESH KUMAR SHARMA",
            "employer_name": "Tech Solutions Pvt Ltd",
            "gross_salary": random.randint(50000, 150000),
            "net_salary": random.randint(40000, 120000),
            "month": "November 2024",
            "deductions": random.randint(5000, 20000),
            "confidence": random.uniform(0.80, 0.95)
        }
        
        logger.info("income_proof_extracted")
        return data


# Global OCR service instance
ocr_service = OCRService()


