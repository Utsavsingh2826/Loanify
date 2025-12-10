"""Analytics and reporting endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.utils.database import get_db
from app.utils.logger import get_logger
from app.services.analytics_service import analytics_service

logger = get_logger(__name__)
router = APIRouter()


@router.get("/conversion-funnel")
async def get_conversion_funnel(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get conversion funnel metrics."""
    try:
        # Default to last 30 days
        if not start_date:
            start = datetime.utcnow() - timedelta(days=30)
        else:
            start = datetime.fromisoformat(start_date)
        
        if not end_date:
            end = datetime.utcnow()
        else:
            end = datetime.fromisoformat(end_date)
        
        funnel = await analytics_service.get_conversion_funnel(db, start, end)
        
        return funnel
        
    except Exception as e:
        logger.error("conversion_funnel_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent-performance")
async def get_agent_performance(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get agent performance metrics."""
    try:
        if not start_date:
            start = datetime.utcnow() - timedelta(days=30)
        else:
            start = datetime.fromisoformat(start_date)
        
        if not end_date:
            end = datetime.utcnow()
        else:
            end = datetime.fromisoformat(end_date)
        
        performance = await analytics_service.get_agent_performance(db, start, end)
        
        return performance
        
    except Exception as e:
        logger.error("agent_performance_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/time-metrics")
async def get_time_metrics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get time-based metrics."""
    try:
        if not start_date:
            start = datetime.utcnow() - timedelta(days=30)
        else:
            start = datetime.fromisoformat(start_date)
        
        if not end_date:
            end = datetime.utcnow()
        else:
            end = datetime.fromisoformat(end_date)
        
        metrics = await analytics_service.get_time_metrics(db, start, end)
        
        return metrics
        
    except Exception as e:
        logger.error("time_metrics_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard_analytics(db: Session = Depends(get_db)):
    """Get complete dashboard analytics."""
    try:
        # Get current month date range
        now = datetime.utcnow()
        start_of_month = datetime(now.year, now.month, 1)
        
        # Get all metrics
        funnel = await analytics_service.get_conversion_funnel(db, start_of_month, now)
        agent_perf = await analytics_service.get_agent_performance(db, start_of_month, now)
        time_metrics = await analytics_service.get_time_metrics(db, start_of_month, now)
        dashboard_stats = await analytics_service.get_dashboard_stats(db)
        
        return {
            "period": {
                "start": start_of_month.isoformat(),
                "end": now.isoformat()
            },
            "overview": dashboard_stats,
            "conversion_funnel": funnel,
            "agent_performance": agent_perf,
            "time_metrics": time_metrics
        }
        
    except Exception as e:
        logger.error("dashboard_analytics_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/applications")
async def export_applications(
    format: str = Query("csv", regex="^(csv|json)$"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export applications data."""
    try:
        from app.models.loan_application import LoanApplication
        
        query = db.query(LoanApplication)
        
        if start_date:
            query = query.filter(LoanApplication.created_at >= datetime.fromisoformat(start_date))
        
        if end_date:
            query = query.filter(LoanApplication.created_at <= datetime.fromisoformat(end_date))
        
        applications = query.all()
        
        # Convert to export format
        data = [
            {
                "application_number": app.application_number,
                "status": app.status.value,
                "requested_amount": float(app.requested_amount) if app.requested_amount else None,
                "approved_amount": float(app.approved_amount) if app.approved_amount else None,
                "credit_score": int(app.credit_score) if app.credit_score else None,
                "created_at": app.created_at.isoformat()
            }
            for app in applications
        ]
        
        if format == "json":
            return {"applications": data}
        else:
            # Return CSV format (simplified)
            import csv
            import io
            
            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            
            return {"csv_data": output.getvalue()}
        
    except Exception as e:
        logger.error("export_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


