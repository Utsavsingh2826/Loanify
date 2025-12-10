"""Credit score checking service (Mock implementation)."""
from typing import Dict, Any
import random
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CreditScoreService:
    """Mock service for credit score checking."""
    
    async def get_credit_score(self, pan_number: str) -> Dict[str, Any]:
        """
        Get credit score from bureau (mock).
        
        In production, this would integrate with CIBIL/Experian APIs.
        """
        try:
            # Mock credit score generation
            # In reality, this would call CIBIL/Experian API
            
            # Generate realistic credit score (550-850)
            score = random.randint(550, 850)
            
            # Determine credit rating
            if score >= 750:
                rating = "Excellent"
                risk_level = "Low"
            elif score >= 700:
                rating = "Good"
                risk_level = "Low"
            elif score >= 650:
                rating = "Fair"
                risk_level = "Medium"
            elif score >= 600:
                rating = "Poor"
                risk_level = "High"
            else:
                rating = "Very Poor"
                risk_level = "Very High"
            
            # Mock credit report data
            credit_data = {
                "score": score,
                "rating": rating,
                "risk_level": risk_level,
                "pan_number": pan_number,
                "report_date": "2024-12-09",
                "accounts": {
                    "total": random.randint(2, 8),
                    "active": random.randint(1, 5),
                    "closed": random.randint(0, 3)
                },
                "credit_utilization": random.randint(20, 80),
                "payment_history": {
                    "on_time_payments": random.randint(85, 100),
                    "late_payments": random.randint(0, 5),
                    "defaults": 0
                },
                "credit_age_months": random.randint(24, 120),
                "recent_inquiries": random.randint(0, 3),
                "total_credit_limit": random.randint(50000, 500000),
                "total_outstanding": random.randint(10000, 200000)
            }
            
            logger.info(
                "credit_score_fetched",
                pan_number=pan_number,
                score=score,
                rating=rating
            )
            
            return credit_data
            
        except Exception as e:
            logger.error("credit_score_error", error=str(e))
            return {
                "score": None,
                "error": str(e)
            }
    
    def interpret_credit_score(self, score: int) -> Dict[str, Any]:
        """Interpret credit score and provide recommendations."""
        if score >= 750:
            return {
                "interpretation": "Excellent credit score! You qualify for the best interest rates.",
                "loan_eligibility": "High",
                "recommended_action": "You can proceed with confidence."
            }
        elif score >= 700:
            return {
                "interpretation": "Good credit score. You qualify for competitive rates.",
                "loan_eligibility": "Good",
                "recommended_action": "You're in a good position for loan approval."
            }
        elif score >= 650:
            return {
                "interpretation": "Fair credit score. You may qualify with moderate interest rates.",
                "loan_eligibility": "Moderate",
                "recommended_action": "Consider improving credit utilization before applying."
            }
        elif score >= 600:
            return {
                "interpretation": "Below average credit score. Higher interest rates may apply.",
                "loan_eligibility": "Limited",
                "recommended_action": "Focus on timely payments to improve score."
            }
        else:
            return {
                "interpretation": "Low credit score. Loan approval may be challenging.",
                "loan_eligibility": "Low",
                "recommended_action": "Work on credit improvement before applying."
            }


# Global credit score service instance
credit_score_service = CreditScoreService()


