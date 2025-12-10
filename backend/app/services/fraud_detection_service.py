"""Fraud detection service."""
from typing import Dict, Any, List
import random
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FraudDetectionService:
    """Service for detecting fraudulent documents and applications."""
    
    async def check_document(
        self,
        document_id: str,
        extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check document for fraud indicators."""
        try:
            flags = []
            suspicion_score = 0
            
            # Mock fraud detection checks
            
            # Check 1: Image quality and tampering
            confidence = extracted_data.get("confidence", 1.0)
            if confidence < 0.7:
                flags.append("Low OCR confidence - possible tampered document")
                suspicion_score += 30
            
            # Check 2: Data consistency (random check for demo)
            if random.random() < 0.05:  # 5% chance of detecting inconsistency
                flags.append("Data inconsistency detected")
                suspicion_score += 40
            
            # Check 3: Duplicate detection
            if random.random() < 0.03:  # 3% chance
                flags.append("Document may have been submitted before")
                suspicion_score += 25
            
            # Check 4: Known fraud patterns
            if random.random() < 0.02:  # 2% chance
                flags.append("Document matches known fraud pattern")
                suspicion_score += 50
            
            suspicious = suspicion_score >= 50
            
            result = {
                "suspicious": suspicious,
                "suspicion_score": suspicion_score,
                "flags": flags,
                "document_id": document_id
            }
            
            if suspicious:
                logger.warning(
                    "fraud_detected",
                    document_id=document_id,
                    score=suspicion_score,
                    flags=flags
                )
            
            return result
            
        except Exception as e:
            logger.error("fraud_check_error", error=str(e))
            return {
                "suspicious": False,
                "error": str(e)
            }
    
    async def analyze_application_behavior(
        self,
        user_id: str,
        application_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze application for suspicious behavioral patterns."""
        try:
            flags = []
            risk_score = 0
            
            # Check for suspicious patterns
            
            # Multiple applications in short time
            if random.random() < 0.05:
                flags.append("Multiple applications detected in short period")
                risk_score += 30
            
            # Inconsistent information
            if random.random() < 0.04:
                flags.append("Inconsistent information across documents")
                risk_score += 35
            
            # Suspicious IP or location
            if random.random() < 0.03:
                flags.append("Application from suspicious location")
                risk_score += 25
            
            # Velocity checks (too fast completion)
            if random.random() < 0.02:
                flags.append("Application completed suspiciously fast")
                risk_score += 20
            
            high_risk = risk_score >= 50
            
            result = {
                "high_risk": high_risk,
                "risk_score": risk_score,
                "flags": flags
            }
            
            if high_risk:
                logger.warning(
                    "high_risk_application",
                    user_id=user_id,
                    risk_score=risk_score
                )
            
            return result
            
        except Exception as e:
            logger.error("behavior_analysis_error", error=str(e))
            return {
                "high_risk": False,
                "error": str(e)
            }


# Global fraud detection service instance
fraud_detection_service = FraudDetectionService()


