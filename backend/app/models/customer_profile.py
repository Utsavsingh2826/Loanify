"""Customer profile model for personalization."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from app.utils.database import Base


class CustomerProfile(Base):
    """Customer profile for personalization and analytics."""
    __tablename__ = "customer_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    
    # Behavioral data
    total_conversations = Column(String, default=0)
    total_applications = Column(String, default=0)
    successful_applications = Column(String, default=0)
    
    # Preferences
    preferred_loan_amount_range = Column(String, nullable=True)
    preferred_tenure = Column(String, nullable=True)
    preferred_communication_time = Column(String, nullable=True)
    preferred_language = Column(String, default="english")
    
    # Sentiment history
    average_sentiment_score = Column(Numeric(5, 2), nullable=True)
    sentiment_history = Column(JSONB, default=[])
    
    # Engagement metrics
    last_engagement_at = Column(DateTime, nullable=True)
    engagement_score = Column(Numeric(5, 2), nullable=True)
    response_time_avg = Column(String, nullable=True)  # in seconds
    
    # Predictive scores
    approval_likelihood = Column(Numeric(5, 2), nullable=True)
    churn_risk_score = Column(Numeric(5, 2), nullable=True)
    lifetime_value_estimate = Column(Numeric(12, 2), nullable=True)
    
    # Interaction patterns
    interaction_patterns = Column(JSONB, default={})
    common_objections = Column(JSONB, default=[])
    common_questions = Column(JSONB, default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional metadata
    metadata = Column(JSONB, default={})
    notes = Column(Text, nullable=True)


