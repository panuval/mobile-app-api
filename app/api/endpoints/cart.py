from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app import models, schemas
from app.db.database import get_db
from app.core.security import oauth2_scheme

router = APIRouter()

@router.get("/", response_model=schemas.CartResponse)
def get_cart(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get the current user's cart
    """
    # Here you would decode the token to get the user_id
    # For simplicity, I'm assuming we have a user_id
    user_id = 123  # This should come from the token
    
    cart_items = db.query(models.CartItem).filter(models.CartItem.customer_id == user_id).all()
    
    items = []
    total_price = 0
    
    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        if product:
            product_description = db.query(models.ProductDescription).filter(
                models.ProductDescription.product_id == item.product_id
            ).first()
            
            price = float(product.price)
            item_total = price * item.quantity
            
            items.append({
                "product_id": item.product_id,
                "name": product_description.name if product_description else "Product",
                "quantity": item.quantity,
                "price": str(price),
                "total_price": str(item_total)
            })
            
            total_price += item_total
    
    return {
        "status": "success",
        "data": {
            "items": items,
            "total_price": str(total_price)
        }
    }

@router.post("/add")
def add_to_cart(
    cart_item: schemas.CartAdd,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Any:
    """
    Add a product to cart
    """
    # Here you would decode the token to get the user_id
    user_id = 123  # This should come from the token
    
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.product_id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if the item is already in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.customer_id == user_id,
        models.CartItem.product_id == cart_item.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += cart_item.quantity
        db.commit()
    else:
        # Add new item
        new_item = models.CartItem(
            customer_id=user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(new_item)
        db.commit()
    
    return {
        "status": "success",
        "message": "Product added to cart"
    }

@router.post("/remove")
def remove_from_cart(
    cart_item: schemas.CartRemove,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Any:
    """
    Remove a product from cart
    """
    # Here you would decode the token to get the user_id
    user_id = 123  # This should come from the token
    
    # Check if the item is in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.customer_id == user_id,
        models.CartItem.product_id == cart_item.product_id
    ).first()
    
    if not existing_item:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    
    # Remove item
    db.delete(existing_item)
    db.commit()
    
    return {
        "status": "success",
        "message": "Product removed from cart"
    }
