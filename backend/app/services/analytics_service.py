"""Analytics service for business intelligence."""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.conversation import Conversation, ConversationStatus
from app.models.loan_application import LoanApplication, ApplicationStatus
from app.models.metrics import ConversionMetric
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AnalyticsService:
    """Service for analytics and metrics."""
    
    async def get_conversion_funnel(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get conversion funnel metrics."""
        try:
            # Total conversations
            total_conversations = db.query(Conversation).filter(
                Conversation.started_at >= start_date,
                Conversation.started_at <= end_date
            ).count()
            
            # Qualified leads (moved past initial engagement)
            qualified = db.query(Conversation).filter(
                Conversation.started_at >= start_date,
                Conversation.started_at <= end_date,
                Conversation.conversation_state.contains({"stage": "qualified"})
            ).count()
            
            # Documents submitted
            docs_submitted = db.query(LoanApplication).filter(
                LoanApplication.created_at >= start_date,
                LoanApplication.created_at <= end_date,
                LoanApplication.status.in_([
                    ApplicationStatus.DOCUMENTS_SUBMITTED,
                    ApplicationStatus.UNDER_VERIFICATION,
                    ApplicationStatus.UNDER_REVIEW,
                    ApplicationStatus.APPROVED,
                    ApplicationStatus.SANCTIONED
                ])
            ).count()
            
            # Applications submitted
            apps_submitted = db.query(LoanApplication).filter(
                LoanApplication.created_at >= start_date,
                LoanApplication.created_at <= end_date,
                LoanApplication.submitted_at.isnot(None)
            ).count()
            
            # Approved
            approved = db.query(LoanApplication).filter(
                LoanApplication.created_at >= start_date,
                LoanApplication.created_at <= end_date,
                LoanApplication.status.in_([
                    ApplicationStatus.APPROVED,
                    ApplicationStatus.SANCTIONED
                ])
            ).count()
            
            # Sanctioned
            sanctioned = db.query(LoanApplication).filter(
                LoanApplication.created_at >= start_date,
                LoanApplication.created_at <= end_date,
                LoanApplication.status == ApplicationStatus.SANCTIONED
            ).count()
            
            # Calculate conversion rates
            funnel = {
                "total_conversations": total_conversations,
                "qualified_leads": qualified,
                "documents_submitted": docs_submitted,
                "applications_submitted": apps_submitted,
                "approved": approved,
                "sanctioned": sanctioned,
                "conversion_rates": {
                    "qualification_rate": (qualified / total_conversations * 100) if total_conversations > 0 else 0,
                    "document_submission_rate": (docs_submitted / qualified * 100) if qualified > 0 else 0,
                    "approval_rate": (approved / apps_submitted * 100) if apps_submitted > 0 else 0,
                    "overall_conversion": (sanctioned / total_conversations * 100) if total_conversations > 0 else 0
                }
            }
            
            return funnel
            
        except Exception as e:
            logger.error("conversion_funnel_error", error=str(e))
            return {}
    
    async def get_agent_performance(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get agent performance metrics."""
        try:
            # Query conversations by current agent
            conversations = db.query(Conversation).filter(
                Conversation.started_at >= start_date,
                Conversation.started_at <= end_date
            ).all()
            
            # Aggregate by agent
            agent_stats = {
                "engage": {"interactions": 0, "handoffs": 0},
                "verify": {"interactions": 0, "handoffs": 0},
                "underwrite": {"interactions": 0, "handoffs": 0},
                "sanction": {"interactions": 0, "handoffs": 0}
            }
            
            for conv in conversations:
                agent = conv.current_agent.value if conv.current_agent else "master"
                if agent in agent_stats:
                    agent_stats[agent]["interactions"] += 1
                    
                    # Check if conversation progressed (successful handoff)
                    if conv.status == ConversationStatus.COMPLETED:
                        agent_stats[agent]["handoffs"] += 1
            
            return agent_stats
            
        except Exception as e:
            logger.error("agent_performance_error", error=str(e))
            return {}
    
    async def get_time_metrics(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get time-based metrics."""
        try:
            applications = db.query(LoanApplication).filter(
                LoanApplication.created_at >= start_date,
                LoanApplication.created_at <= end_date,
                LoanApplication.sanctioned_at.isnot(None)
            ).all()
            
            if not applications:
                return {
                    "avg_time_to_sanction_minutes": 0,
                    "min_time_minutes": 0,
                    "max_time_minutes": 0
                }
            
            times = []
            for app in applications:
                time_diff = (app.sanctioned_at - app.created_at).total_seconds() / 60
                times.append(time_diff)
            
            return {
                "avg_time_to_sanction_minutes": sum(times) / len(times),
                "min_time_minutes": min(times),
                "max_time_minutes": max(times),
                "median_time_minutes": sorted(times)[len(times) // 2]
            }
            
        except Exception as e:
            logger.error("time_metrics_error", error=str(e))
            return {}
    
    async def get_dashboard_stats(
        self,
        db: Session
    ) -> Dict[str, Any]:
        """Get dashboard statistics."""
        try:
            today = datetime.utcnow().date()
            
            # Today's stats
            today_conversations = db.query(Conversation).filter(
                Conversation.started_at >= datetime.combine(today, datetime.min.time())
            ).count()
            
            today_applications = db.query(LoanApplication).filter(
                LoanApplication.created_at >= datetime.combine(today, datetime.min.time())
            ).count()
            
            # Total stats
            total_conversations = db.query(Conversation).count()
            total_applications = db.query(LoanApplication).count()
            total_sanctioned = db.query(LoanApplication).filter(
                LoanApplication.status == ApplicationStatus.SANCTIONED
            ).count()
            
            # Active conversations
            active_conversations = db.query(Conversation).filter(
                Conversation.status == ConversationStatus.ACTIVE
            ).count()
            
            return {
                "today": {
                    "conversations": today_conversations,
                    "applications": today_applications
                },
                "total": {
                    "conversations": total_conversations,
                    "applications": total_applications,
                    "sanctioned": total_sanctioned
                },
                "active_conversations": active_conversations,
                "conversion_rate": (total_sanctioned / total_conversations * 100) if total_conversations > 0 else 0
            }
            
        except Exception as e:
            logger.error("dashboard_stats_error", error=str(e))
            return {}


# Global analytics service instance
analytics_service = AnalyticsService()


