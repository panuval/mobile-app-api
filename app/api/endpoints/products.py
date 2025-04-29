from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from app import models
from app.db.database import get_db

router = APIRouter()

@router.get("/")
def get_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None
) -> Any:
    """
    Retrieve all products with pagination
    """
    try:
        # Calculate skip for pagination
        skip = (page - 1) * limit
        
        # Base query - only active products
        query = db.query(models.Product).filter(models.Product.status == 1)
        
        # Apply category filter if provided
        if category_id:
            query = query.join(models.ProductToCategory).filter(
                models.ProductToCategory.category_id == category_id
            )
        
        # Get total count
        total_count = query.count()
        
        # Get products with pagination
        products = query.offset(skip).limit(limit).all()
        
        # Build response
        result = []
        for product in products:
            # Get product description (assuming English is language_id 1)
            description = db.query(models.ProductDescription).filter(
                models.ProductDescription.product_id == product.product_id,
                models.ProductDescription.language_id == 1
            ).first()
            
            # Determine stock status
            stock_status = "OUT_OF_STOCK"
            if product.quantity > 0:
                stock_status = "IN_STOCK"
                
            # Format the product data according to ItemSummary schema
            product_data = {
                "itemId": product.product_id,
                "name": description.name if description else "",
                "price": float(product.price),
                "imageUrl": f"https://assets2.panuval.com/image/cache/catalog/{product.image}" if product.image else None,
                "stockStatus": stock_status,
                "originalPrice": None,
                "discountPercentage": None,
                "label": {
                    "label": None,
                    "showLabel": False,
                    "labelType": "NONE"
                }
            }
            result.append(product_data)
        
        return {
            "displayText": "Products",
            "items": result,
            "pagination": {
                "currentPage": page,
                "pageSize": limit,
                "totalItems": total_count,
                "totalPages": (total_count + limit - 1) // limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@router.get("/{product_id}")
def get_product_details(
    product_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get details of a specific product
    """
    try:
        # Get the product
        product = db.query(models.Product).filter(
            models.Product.product_id == product_id
        ).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get product description
        description = db.query(models.ProductDescription).filter(
            models.ProductDescription.product_id == product_id,
            models.ProductDescription.language_id == 1  # Assuming language_id 1 is default
        ).first()
        
        # Build the response
        product_data = {
            "product_id": product.product_id,
            "name": description.name if description else "",
            "price": str(product.price),
            "image": f"https://assets2.panuval.com/image/cache/catalog/{product.image}" if product.image else "",
            "description": description.description if description else "",
            "quantity": product.quantity,
            "rating": 0.0  # Default rating if not available
        }
        
        # Try to get product rating if available (from reviews perhaps)
        try:
            reviews = db.query(models.Review).filter(
                models.Review.product_id == product_id,
                models.Review.status == 1
            ).all()
            
            if reviews:
                total_rating = sum(review.rating for review in reviews)
                avg_rating = total_rating / len(reviews)
                product_data["rating"] = float(avg_rating)
        except:
            # If there's an error getting ratings, just use the default
            pass
        
        return {
            "status": "success",
            "data": product_data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")