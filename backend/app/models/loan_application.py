"""Loan application data models."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Boolean, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
import enum
from app.utils.database import Base


class ApplicationStatus(str, enum.Enum):
    """Application status enum."""
    INITIATED = "initiated"
    DOCUMENTS_PENDING = "documents_pending"
    DOCUMENTS_SUBMITTED = "documents_submitted"
    UNDER_VERIFICATION = "under_verification"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SANCTIONED = "sanctioned"


class LoanPurpose(str, enum.Enum):
    """Loan purpose enum."""
    PERSONAL = "personal"
    EDUCATION = "education"
    MEDICAL = "medical"
    WEDDING = "wedding"
    TRAVEL = "travel"
    HOME_RENOVATION = "home_renovation"
    DEBT_CONSOLIDATION = "debt_consolidation"
    BUSINESS = "business"
    OTHER = "other"


class LoanApplication(Base):
    """Loan application model."""
    __tablename__ = "loan_applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_number = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    
    # Application Status
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.INITIATED)
    
    # Loan Details
    loan_purpose = Column(Enum(LoanPurpose), nullable=True)
    requested_amount = Column(Numeric(12, 2), nullable=True)
    approved_amount = Column(Numeric(12, 2), nullable=True)
    tenure_months = Column(String, nullable=True)
    interest_rate = Column(Numeric(5, 2), nullable=True)
    
    # Applicant Financial Details
    monthly_income = Column(Numeric(12, 2), nullable=True)
    existing_emis = Column(Numeric(12, 2), nullable=True)
    credit_score = Column(String, nullable=True)
    
    # Risk Assessment
    risk_score = Column(Numeric(5, 2), nullable=True)
    risk_category = Column(String, nullable=True)  # low, medium, high
    eligibility_amount = Column(Numeric(12, 2), nullable=True)
    
    # Documents Status
    documents_submitted = Column(JSONB, default={})
    documents_verified = Column(JSONB, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    sanctioned_at = Column(DateTime, nullable=True)
    
    # Sanction Letter
    sanction_letter_url = Column(String, nullable=True)
    sanction_letter_generated_at = Column(DateTime, nullable=True)
    
    # Additional metadata
    app_metadata = Column(JSONB, default={})
    notes = Column(Text, nullable=True)


class Document(Base):
    """Document model."""
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("loan_applications.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Document details
    document_type = Column(String, nullable=False)  # pan, aadhaar, bank_statement, etc.
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    
    # Verification status
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    verification_notes = Column(Text, nullable=True)
    
    # Extracted data from OCR
    extracted_data = Column(JSONB, default={})
    confidence_score = Column(Numeric(5, 2), nullable=True)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Fraud detection
    fraud_flags = Column(JSONB, default=[])
    is_suspicious = Column(Boolean, default=False)


