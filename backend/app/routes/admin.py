"""Admin endpoints for application and user management."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.utils.database import get_db
from app.utils.logger import get_logger
from app.models.user import User
from app.models.loan_application import LoanApplication, ApplicationStatus
from app.models.conversation import Conversation

logger = get_logger(__name__)
router = APIRouter()


# Response models
class ApplicationListItem(BaseModel):
    id: str
    application_number: str
    user_id: str
    status: str
    loan_amount: Optional[float]
    created_at: datetime
    updated_at: datetime


class ApplicationDetail(BaseModel):
    id: str
    application_number: str
    user: dict
    status: str
    loan_purpose: Optional[str]
    requested_amount: Optional[float]
    approved_amount: Optional[float]
    interest_rate: Optional[float]
    tenure_months: Optional[int]
    monthly_income: Optional[float]
    credit_score: Optional[int]
    risk_category: Optional[str]
    created_at: datetime
    documents: List[dict]


@router.get("/applications", response_model=List[ApplicationListItem])
async def list_applications(
    status: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all loan applications with filtering."""
    try:
        query = db.query(LoanApplication)
        
        if status:
            query = query.filter(LoanApplication.status == status)
        
        applications = query.order_by(
            LoanApplication.created_at.desc()
        ).limit(limit).offset(offset).all()
        
        return [
            ApplicationListItem(
                id=str(app.id),
                application_number=app.application_number,
                user_id=str(app.user_id),
                status=app.status.value,
                loan_amount=float(app.requested_amount) if app.requested_amount else None,
                created_at=app.created_at,
                updated_at=app.updated_at
            )
            for app in applications
        ]
        
    except Exception as e:
        logger.error("list_applications_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/applications/{application_id}", response_model=ApplicationDetail)
async def get_application_detail(
    application_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed application information."""
    try:
        application = db.query(LoanApplication).filter(
            LoanApplication.id == application_id
        ).first()
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Get user details
        user = db.query(User).filter(User.id == application.user_id).first()
        
        user_data = {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone
        } if user else {}
        
        # Get documents
        from app.models.loan_application import Document
        documents = db.query(Document).filter(
            Document.application_id == application_id
        ).all()
        
        docs_data = [
            {
                "id": str(doc.id),
                "document_type": doc.document_type,
                "filename": doc.file_name,
                "is_verified": doc.is_verified,
                "uploaded_at": doc.uploaded_at.isoformat()
            }
            for doc in documents
        ]
        
        return ApplicationDetail(
            id=str(application.id),
            application_number=application.application_number,
            user=user_data,
            status=application.status.value,
            loan_purpose=application.loan_purpose.value if application.loan_purpose else None,
            requested_amount=float(application.requested_amount) if application.requested_amount else None,
            approved_amount=float(application.approved_amount) if application.approved_amount else None,
            interest_rate=float(application.interest_rate) if application.interest_rate else None,
            tenure_months=int(application.tenure_months) if application.tenure_months else None,
            monthly_income=float(application.monthly_income) if application.monthly_income else None,
            credit_score=int(application.credit_score) if application.credit_score else None,
            risk_category=application.risk_category,
            created_at=application.created_at,
            documents=docs_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_application_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/applications/{application_id}/status")
async def update_application_status(
    application_id: str,
    new_status: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update application status."""
    try:
        application = db.query(LoanApplication).filter(
            LoanApplication.id == application_id
        ).first()
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Validate status
        try:
            status_enum = ApplicationStatus[new_status.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        application.status = status_enum
        if notes:
            application.notes = notes
        
        application.updated_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(
            "application_status_updated",
            application_id=application_id,
            new_status=new_status
        )
        
        return {
            "success": True,
            "application_id": application_id,
            "new_status": new_status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("update_status_error", error=str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users")
async def list_users(
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all users."""
    try:
        users = db.query(User).order_by(
            User.created_at.desc()
        ).limit(limit).offset(offset).all()
        
        return {
            "users": [
                {
                    "id": str(user.id),
                    "full_name": user.full_name,
                    "email": user.email,
                    "phone": user.phone,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat()
                }
                for user in users
            ]
        }
        
    except Exception as e:
        logger.error("list_users_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
async def list_conversations(
    status: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all conversations."""
    try:
        query = db.query(Conversation)
        
        if status:
            from app.models.conversation import ConversationStatus
            query = query.filter(Conversation.status == ConversationStatus[status.upper()])
        
        conversations = query.order_by(
            Conversation.started_at.desc()
        ).limit(limit).offset(offset).all()
        
        return {
            "conversations": [
                {
                    "id": str(conv.id),
                    "user_id": str(conv.user_id),
                    "status": conv.status.value,
                    "current_agent": conv.current_agent.value,
                    "message_count": conv.message_count,
                    "started_at": conv.started_at.isoformat(),
                    "last_message_at": conv.last_message_at.isoformat() if conv.last_message_at else None
                }
                for conv in conversations
            ]
        }
        
    except Exception as e:
        logger.error("list_conversations_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/overview")
async def get_overview_stats(db: Session = Depends(get_db)):
    """Get overview statistics."""
    try:
        from app.services.analytics_service import analytics_service
        
        stats = await analytics_service.get_dashboard_stats(db)
        
        return stats
        
    except Exception as e:
        logger.error("overview_stats_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


