"""Metrics and analytics models."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from app.utils.database import Base


class ConversionMetric(Base):
    """Conversion metrics model."""
    __tablename__ = "conversion_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Funnel metrics
    total_conversations = Column(String, default=0)
    qualified_leads = Column(String, default=0)
    documents_submitted = Column(String, default=0)
    applications_submitted = Column(String, default=0)
    applications_approved = Column(String, default=0)
    sanctioned = Column(String, default=0)
    
    # Conversion rates
    qualification_rate = Column(Numeric(5, 2), default=0)
    document_submission_rate = Column(Numeric(5, 2), default=0)
    approval_rate = Column(Numeric(5, 2), default=0)
    overall_conversion_rate = Column(Numeric(5, 2), default=0)
    
    # Time metrics (in minutes)
    avg_time_to_qualification = Column(Numeric(10, 2), nullable=True)
    avg_time_to_document_submission = Column(Numeric(10, 2), nullable=True)
    avg_time_to_sanction = Column(Numeric(10, 2), nullable=True)
    
    # Agent performance
    agent_performance = Column(JSONB, default={})


class AgentPerformance(Base):
    """Agent performance metrics."""
    __tablename__ = "agent_performance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_type = Column(String, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Performance metrics
    total_interactions = Column(String, default=0)
    successful_handoffs = Column(String, default=0)
    failed_handoffs = Column(String, default=0)
    avg_response_time = Column(Numeric(10, 2), nullable=True)
    
    # Quality metrics
    avg_sentiment_score = Column(Numeric(5, 2), nullable=True)
    customer_satisfaction = Column(Numeric(5, 2), nullable=True)
    
    # Specific metrics
    metrics_data = Column(JSONB, default={})


class ABTest(Base):
    """A/B testing model."""
    __tablename__ = "ab_tests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    
    # Test configuration
    is_active = Column(Boolean, default=True)
    variant_a_config = Column(JSONB, default={})
    variant_b_config = Column(JSONB, default={})
    
    # Results
    variant_a_conversions = Column(String, default=0)
    variant_a_total = Column(String, default=0)
    variant_b_conversions = Column(String, default=0)
    variant_b_total = Column(String, default=0)
    
    # Statistical significance
    p_value = Column(Numeric(5, 4), nullable=True)
    is_significant = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)


