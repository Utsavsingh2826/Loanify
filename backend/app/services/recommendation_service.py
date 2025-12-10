"""Recommendation engine for loan products."""
from typing import Dict, Any, List
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RecommendationService:
    """Service for loan product recommendations."""
    
    def recommend_loan_product(
        self,
        loan_purpose: str,
        requested_amount: float,
        credit_score: int,
        monthly_income: float
    ) -> Dict[str, Any]:
        """Recommend best loan product for customer."""
        try:
            # Product definitions
            products = {
                "quick_loan": {
                    "name": "Quick Loan",
                    "min_amount": 10000,
                    "max_amount": 200000,
                    "min_credit_score": 650,
                    "interest_rate_range": "12% - 26%",
                    "features": ["Instant approval", "Minimal documentation", "Quick disbursal"]
                },
                "personal_loan_standard": {
                    "name": "Personal Loan Standard",
                    "min_amount": 50000,
                    "max_amount": 2500000,
                    "min_credit_score": 650,
                    "interest_rate_range": "10.5% - 24%",
                    "features": ["Flexible tenure", "Competitive rates", "No collateral"]
                },
                "premium_personal_loan": {
                    "name": "Premium Personal Loan",
                    "min_amount": 500000,
                    "max_amount": 4000000,
                    "min_credit_score": 750,
                    "interest_rate_range": "9.5% - 18%",
                    "features": ["Best rates", "Priority service", "Higher amounts"]
                }
            }
            
            # Recommend based on criteria
            recommendations = []
            
            for product_id, product in products.items():
                # Check eligibility
                if credit_score < product["min_credit_score"]:
                    continue
                
                if requested_amount < product["min_amount"]:
                    continue
                
                if requested_amount > product["max_amount"]:
                    continue
                
                # Calculate suitability score
                score = 0
                
                # Amount match
                if product["min_amount"] <= requested_amount <= product["max_amount"]:
                    score += 40
                
                # Credit score bonus
                if credit_score >= 750:
                    score += 30
                elif credit_score >= 700:
                    score += 20
                else:
                    score += 10
                
                # Income adequacy
                emi_percentage = (requested_amount * 0.02) / monthly_income * 100  # Rough EMI estimate
                if emi_percentage < 40:
                    score += 30
                elif emi_percentage < 50:
                    score += 20
                else:
                    score += 10
                
                recommendations.append({
                    "product_id": product_id,
                    "product_name": product["name"],
                    "suitability_score": score,
                    "details": product
                })
            
            # Sort by suitability score
            recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
            
            result = {
                "recommended_product": recommendations[0] if recommendations else None,
                "all_options": recommendations
            }
            
            logger.info(
                "product_recommended",
                product=recommendations[0]["product_name"] if recommendations else None
            )
            
            return result
            
        except Exception as e:
            logger.error("recommendation_error", error=str(e))
            return {
                "recommended_product": None,
                "error": str(e)
            }
    
    def recommend_tenure(
        self,
        loan_amount: float,
        monthly_income: float,
        existing_emis: float
    ) -> Dict[str, Any]:
        """Recommend optimal loan tenure."""
        try:
            # Calculate comfortable EMI (40% of disposable income)
            disposable_income = monthly_income - existing_emis
            comfortable_emi = disposable_income * 0.4
            
            # Calculate tenure for different scenarios
            tenures = []
            for months in [12, 24, 36, 48, 60]:
                # Assuming average interest rate of 15%
                rate = 0.15 / 12
                emi = (loan_amount * rate * (1 + rate) ** months) / ((1 + rate) ** months - 1)
                
                affordability = "comfortable" if emi <= comfortable_emi else "tight"
                
                tenures.append({
                    "months": months,
                    "years": months / 12,
                    "monthly_emi": round(emi, 2),
                    "total_interest": round((emi * months) - loan_amount, 2),
                    "total_payable": round(emi * months, 2),
                    "affordability": affordability
                })
            
            # Find recommended tenure (longest comfortable tenure)
            recommended = None
            for tenure in reversed(tenures):
                if tenure["affordability"] == "comfortable":
                    recommended = tenure
                    break
            
            if not recommended:
                recommended = tenures[0]  # Shortest tenure if none comfortable
            
            return {
                "recommended_tenure": recommended,
                "all_options": tenures
            }
            
        except Exception as e:
            logger.error("tenure_recommendation_error", error=str(e))
            return {
                "recommended_tenure": None,
                "error": str(e)
            }


# Global recommendation service instance
recommendation_service = RecommendationService()


