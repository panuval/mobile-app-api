from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db.database import get_db
from app.core.security import oauth2_scheme

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_active_offers(
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve all active offers
    """
    offers = db.query(models.Offer).filter(models.Offer.status == 1).all()
    
    result = []
    for offer in offers:
        result.append({
            "offer_id": offer.offer_id,
            "title": offer.title,
            "discount_type": offer.discount_type,
            "discount_value": offer.discount_value,
            "start_date": offer.start_date,
            "end_date": offer.end_date,
            "status": offer.status
        })
    
    return result

@router.get("/{offer_id}", response_model=dict)
def get_offer_by_id(
    offer_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get a specific offer by ID
    """
    offer = db.query(models.Offer).filter(
        models.Offer.offer_id == offer_id
    ).first()
    
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    return {
        "offer_id": offer.offer_id,
        "title": offer.title,
        "discount_type": offer.discount_type,
        "discount_value": offer.discount_value,
        "start_date": offer.start_date,
        "end_date": offer.end_date,
        "status": offer.status
    }