from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db.database import get_db
from app.core.security import oauth2_scheme

router = APIRouter()

@router.get("/{product_id}", response_model=List[dict])
def get_product_reviews(
    product_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve reviews for a specific product
    """
    reviews = db.query(models.Review).filter(
        models.Review.product_id == product_id,
        models.Review.status == 1
    ).all()
    
    result = []
    for review in reviews:
        result.append({
            "review_id": review.review_id,
            "customer_name": review.customer_name,
            "rating": review.rating,
            "comment": review.comment
        })
    
    return result

@router.get("/single/{review_id}", response_model=dict)
def get_review_by_id(
    review_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get a specific review by ID
    """
    review = db.query(models.Review).filter(
        models.Review.review_id == review_id
    ).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {
        "review_id": review.review_id,
        "customer_name": review.customer_name,
        "rating": review.rating,
        "comment": review.comment
    }