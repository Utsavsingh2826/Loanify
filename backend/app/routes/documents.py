"""Document upload and management endpoints."""
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.utils.database import get_db
from app.utils.logger import get_logger
from app.models.loan_application import Document
from app.services.document_service import document_service
from app.config import settings

logger = get_logger(__name__)
router = APIRouter()


# Response models
class DocumentUploadResponse(BaseModel):
    success: bool
    document_id: str
    filename: str
    document_type: str
    message: str


class DocumentVerificationResponse(BaseModel):
    document_id: str
    document_type: str
    valid: bool
    extracted_data: dict
    confidence_score: float
    fraud_flags: List[str]


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    user_id: str = Form(...),
    application_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload a document."""
    try:
        # Validate file size
        file_content = await file.read()
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds maximum allowed"
            )
        
        # Save document
        save_result = await document_service.save_document(
            file_content=file_content,
            filename=file.filename,
            document_type=document_type,
            user_id=user_id
        )
        
        if not save_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save document"
            )
        
        # Create document record
        document = Document(
            id=uuid.uuid4(),
            application_id=application_id,
            user_id=user_id,
            document_type=document_type,
            file_name=file.filename,
            file_path=save_result["file_path"],
            file_size=len(file_content),
            mime_type=file.content_type or "application/octet-stream"
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        logger.info(
            "document_uploaded",
            document_id=str(document.id),
            document_type=document_type,
            user_id=user_id
        )
        
        return DocumentUploadResponse(
            success=True,
            document_id=str(document.id),
            filename=file.filename,
            document_type=document_type,
            message="Document uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("document_upload_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify/{document_id}", response_model=DocumentVerificationResponse)
async def verify_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Verify a document."""
    try:
        # Get document
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Verify document
        verification_result = await document_service.verify_document(
            document_id=str(document.id),
            document_type=document.document_type
        )
        
        # Update document record
        document.is_verified = verification_result["valid"]
        document.verified_at = datetime.utcnow() if verification_result["valid"] else None
        document.extracted_data = verification_result.get("extracted_data", {})
        document.confidence_score = verification_result.get("confidence_score", 0)
        document.fraud_flags = verification_result.get("fraud_flags", [])
        document.is_suspicious = len(verification_result.get("fraud_flags", [])) > 0
        
        db.commit()
        
        logger.info(
            "document_verified",
            document_id=document_id,
            valid=verification_result["valid"]
        )
        
        return DocumentVerificationResponse(
            document_id=document_id,
            document_type=document.document_type,
            valid=verification_result["valid"],
            extracted_data=verification_result.get("extracted_data", {}),
            confidence_score=verification_result.get("confidence_score", 0),
            fraud_flags=verification_result.get("fraud_flags", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("document_verification_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/application/{application_id}")
async def get_application_documents(
    application_id: str,
    db: Session = Depends(get_db)
):
    """Get all documents for an application."""
    try:
        documents = db.query(Document).filter(
            Document.application_id == application_id
        ).all()
        
        return {
            "application_id": application_id,
            "documents": [
                {
                    "id": str(doc.id),
                    "document_type": doc.document_type,
                    "filename": doc.file_name,
                    "uploaded_at": doc.uploaded_at.isoformat(),
                    "is_verified": doc.is_verified,
                    "verified_at": doc.verified_at.isoformat() if doc.verified_at else None,
                    "is_suspicious": doc.is_suspicious
                }
                for doc in documents
            ]
        }
        
    except Exception as e:
        logger.error("get_documents_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Delete a document."""
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete file from storage (implement if needed)
        
        # Delete database record
        db.delete(document)
        db.commit()
        
        logger.info("document_deleted", document_id=document_id)
        
        return {"success": True, "message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("document_delete_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


