"""Customer profiling service for personalization."""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.customer_profile import CustomerProfile
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProfilingService:
    """Service for customer profiling and personalization."""
    
    async def get_or_create_profile(
        self,
        user_id: str,
        db: Session
    ) -> CustomerProfile:
        """Get existing profile or create new one."""
        try:
            profile = db.query(CustomerProfile).filter(
                CustomerProfile.user_id == user_id
            ).first()
            
            if not profile:
                profile = CustomerProfile(user_id=user_id)
                db.add(profile)
                db.commit()
                db.refresh(profile)
                logger.info("profile_created", user_id=user_id)
            
            return profile
            
        except Exception as e:
            logger.error("profile_creation_error", error=str(e))
            db.rollback()
            raise
    
    async def update_engagement_metrics(
        self,
        user_id: str,
        db: Session,
        sentiment_score: Optional[float] = None
    ) -> None:
        """Update engagement metrics for user."""
        try:
            profile = await self.get_or_create_profile(user_id, db)
            
            # Update engagement
            profile.last_engagement_at = datetime.utcnow()
            profile.total_conversations += 1
            
            # Update sentiment history
            if sentiment_score is not None:
                sentiment_history = profile.sentiment_history or []
                sentiment_history.append({
                    "score": sentiment_score,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
                # Keep last 50 records
                profile.sentiment_history = sentiment_history[-50:]
                
                # Calculate average
                scores = [s["score"] for s in sentiment_history]
                profile.average_sentiment_score = sum(scores) / len(scores)
            
            db.commit()
            
        except Exception as e:
            logger.error("engagement_update_error", error=str(e))
            db.rollback()
    
    async def update_application_metrics(
        self,
        user_id: str,
        db: Session,
        application_successful: bool = False
    ) -> None:
        """Update application metrics."""
        try:
            profile = await self.get_or_create_profile(user_id, db)
            
            profile.total_applications += 1
            if application_successful:
                profile.successful_applications += 1
            
            db.commit()
            
        except Exception as e:
            logger.error("application_metrics_error", error=str(e))
            db.rollback()
    
    async def calculate_approval_likelihood(
        self,
        user_id: str,
        db: Session,
        credit_score: int,
        monthly_income: float,
        existing_emis: float
    ) -> float:
        """Calculate likelihood of loan approval."""
        try:
            # Simple scoring model
            score = 0.0
            
            # Credit score component (40%)
            if credit_score >= 750:
                score += 0.4
            elif credit_score >= 700:
                score += 0.3
            elif credit_score >= 650:
                score += 0.2
            else:
                score += 0.1
            
            # DTI component (30%)
            dti = (existing_emis / monthly_income) * 100 if monthly_income > 0 else 100
            if dti < 35:
                score += 0.3
            elif dti < 45:
                score += 0.2
            else:
                score += 0.1
            
            # Income component (20%)
            if monthly_income >= 75000:
                score += 0.2
            elif monthly_income >= 50000:
                score += 0.15
            elif monthly_income >= 30000:
                score += 0.1
            
            # Historical performance (10%)
            profile = await self.get_or_create_profile(user_id, db)
            if profile.successful_applications > 0:
                success_rate = profile.successful_applications / profile.total_applications
                score += success_rate * 0.1
            else:
                score += 0.05  # Neutral for new customers
            
            # Update profile
            profile.approval_likelihood = score
            db.commit()
            
            return score
            
        except Exception as e:
            logger.error("approval_likelihood_error", error=str(e))
            return 0.5


# Global profiling service instance
profiling_service = ProfilingService()


