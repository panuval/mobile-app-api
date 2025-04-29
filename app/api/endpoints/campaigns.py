from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db.database import get_db
from app.core.security import oauth2_scheme

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_active_campaigns(
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve all active marketing campaigns
    """
    campaigns = db.query(models.Campaign).filter(models.Campaign.status == 1).all()
    
    result = []
    for campaign in campaigns:
        result.append({
            "campaign_id": campaign.campaign_id,
            "title": campaign.title,
            "start_date": campaign.start_date,
            "end_date": campaign.end_date,
            "status": campaign.status
        })
    
    return result

@router.get("/{campaign_id}", response_model=dict)
def get_campaign_by_id(
    campaign_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get a specific campaign by ID
    """
    campaign = db.query(models.Campaign).filter(
        models.Campaign.campaign_id == campaign_id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {
        "campaign_id": campaign.campaign_id,
        "title": campaign.title,
        "start_date": campaign.start_date,
        "end_date": campaign.end_date,
        "status": campaign.status
    }