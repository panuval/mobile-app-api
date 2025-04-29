from typing import Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app import models, schemas
from app.db.database import get_db
from app.schemas.layout import ItemDetail, ItemSearchResponse

router = APIRouter()

@router.get("/search")
def search_items(
    q: Optional[str] = Query(None, description="Search keyword"),
    category_id: Optional[List[str]] = Query(None, description="Filter by category IDs"),
    author_id: Optional[List[str]] = Query(None, description="Filter by author IDs"),
    publisher_id: Optional[List[str]] = Query(None, description="Filter by publisher IDs"),
    price_min: Optional[float] = Query(None, description="Minimum price"),
    price_max: Optional[float] = Query(None, description="Maximum price"),
    exclude_out_of_stock: bool = Query(False, description="Exclude out of stock items"),
    sort_by: str = Query("relevance", description="Sort criteria"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Search and filter items with pagination and sorting.
    """
    try:
        # Calculate offset for pagination
        offset = (page - 1) * page_size
        
        # Start with base query for active products
        query = db.query(models.Product).join(
            models.ProductDescription, 
            models.Product.product_id == models.ProductDescription.product_id
        ).filter(models.Product.status == 1)
        
        # Apply keyword search if provided
        if q:
            search_term = f"%{q}%"
            query = query.filter(
                or_(
                    models.ProductDescription.name.ilike(search_term),
                    models.ProductDescription.description.ilike(search_term),
                    models.ProductDescription.meta_keyword.ilike(search_term),
                    models.Product.model.ilike(search_term),
                    models.Product.sku.ilike(search_term)
                )
            )
        
        # Apply category filter if provided
        if category_id:
            query = query.join(
                models.ProductToCategory,
                models.Product.product_id == models.ProductToCategory.product_id
            ).filter(models.ProductToCategory.category_id.in_([int(cid) for cid in category_id]))
            
        # Apply author filter if provided (commented out until tables exist)
        # if author_id:
        #     query = query.join(
        #         models.ProductAuthor,
        #         models.Product.product_id == models.ProductAuthor.product_id
        #     ).filter(models.ProductAuthor.author_id.in_([int(aid) for aid in author_id]))
            
        # Apply publisher filter if provided (commented out until tables exist)
        # if publisher_id:
        #     query = query.join(
        #         models.ProductPublisher,
        #         models.Product.product_id == models.ProductPublisher.product_id
        #     ).filter(models.ProductPublisher.publisher_id.in_([int(pid) for pid in publisher_id]))
        
        # Apply price filters if provided
        if price_min is not None:
            query = query.filter(models.Product.price >= price_min)
        if price_max is not None:
            query = query.filter(models.Product.price <= price_max)
        
        # Apply stock filter if requested
        if exclude_out_of_stock:
            query = query.filter(models.Product.quantity > 0)
        
        # Apply sorting
        if sort_by == "price_asc":
            query = query.order_by(models.Product.price.asc())
        elif sort_by == "price_desc":
            query = query.order_by(models.Product.price.desc())
        elif sort_by == "name_asc":
            query = query.order_by(models.ProductDescription.name.asc())
        elif sort_by == "name_desc":
            query = query.order_by(models.ProductDescription.name.desc())
        elif sort_by == "year_newest":
            query = query.order_by(models.Product.date_added.desc())
        elif sort_by == "year_oldest":
            query = query.order_by(models.Product.date_added.asc())
        # For "relevance" and "best_sellers", default to most viewed or recently added
        else:
            if sort_by == "best_sellers":
                query = query.order_by(models.Product.viewed.desc())
            else:  # Default sorting is by date added (newest first)
                query = query.order_by(models.Product.date_added.desc())
        
        # Get total count for pagination
        total_count = query.count()
        
        # Apply pagination
        items = query.offset(offset).limit(page_size).all()
        
        # Build response
        result = []
        for product in items:
            # Get product description
            description = db.query(models.ProductDescription).filter(
                models.ProductDescription.product_id == product.product_id,
                models.ProductDescription.language_id == 1  # Assuming language_id 1 is default
            ).first()
            
            if not description:
                continue
                
            # Determine stock status
            stock_status = "OUT_OF_STOCK"
            if product.quantity > 0:
                stock_status = "IN_STOCK"
            
            # Calculate price
            price = float(product.price)
            
            # Since original_price column doesn't exist yet, we'll use a workaround
            # In a real implementation, you'd fetch this from a discount table or calculate it
            original_price = None
            discount_percentage = None
            
            # For demo purposes, let's simulate a 10% discount on some products
            if product.product_id % 3 == 0:  # Apply to every 3rd product for demo
                original_price = round(price * 1.1, 2)  # 10% higher than current price
                discount_percentage = 10
            
            # Get the corresponding one_items entry
            one_item = db.query(models.OneItems).filter(
                models.OneItems.oc_id == product.product_id
            ).first()
            
            # Use one_items.id if available, otherwise fallback to product.product_id
            item_id = one_item.id if one_item else product.product_id
            
            # Add product to results
            result.append({
                "itemId": item_id,
                "name": description.name,
                "imageUrl": f"https://assets2.panuval.com/image/cache/catalog/{product.image}" if product.image else None,
                "price": price,
                "originalPrice": original_price,
                "discountPercentage": discount_percentage,
                "stockStatus": stock_status
            })
        
        # Build pagination info
        pagination = {
            "currentPage": page,
            "pageSize": page_size,
            "totalItems": total_count,
            "totalPages": (total_count + page_size - 1) // page_size
        }
        
        # Construct display text
        display_text = "All Items"
        if q:
            display_text = f"Search results for '{q}'"
        elif category_id and len(category_id) == 1:
            # Try to get category name if only one category is selected
            try:
                category = db.query(models.Category).filter(
                    models.Category.category_id == int(category_id[0])
                ).first()
                if category:
                    # Get category description for the name
                    category_description = db.query(models.CategoryDescription).filter(
                        models.CategoryDescription.category_id == category.category_id,
                        models.CategoryDescription.language_id == 1  # Assuming language_id 1 is default
                    ).first()
                    display_text = category_description.name if category_description else f"Category {category.category_id}"
            except:
                pass
        
        return {
            "displayText": display_text,
            "items": result,
            "pagination": pagination
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching items: {str(e)}")

@router.get("/{item_id}")
def get_item_detail(
    item_id: int = Path(..., description="The ID of the item to retrieve"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get detailed information about a specific item by its ID.
    """
    try:
        # Check if the item_id is from one_items table
        one_item = db.query(models.OneItems).filter(
            models.OneItems.id == item_id
        ).first()
        
        # If found in one_items, use oc_id to get the product
        if one_item:
            product_id = one_item.oc_id
        else:
            # Fallback to using item_id directly as product_id
            product_id = item_id
            
        # Get the product
        product = db.query(models.Product).filter(
            models.Product.product_id == product_id,
            models.Product.status == 1
        ).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Get product description
        description = db.query(models.ProductDescription).filter(
            models.ProductDescription.product_id == product_id,
            models.ProductDescription.language_id == 1  # Assuming language_id 1 is default
        ).first()
        
        if not description:
            raise HTTPException(status_code=404, detail="Item description not found")
        
        # Determine stock status
        stock_status = "OUT_OF_STOCK"
        if product.quantity > 0:
            stock_status = "IN_STOCK"
        
        # Calculate price
        price = float(product.price)
        
        # Since original_price column doesn't exist yet, we'll use a workaround
        # In a real implementation, you'd fetch this from a discount table or calculate it
        original_price = None
        discount_percentage = None
        
        # For demo purposes, let's simulate a 10% discount on some products
        if product.product_id % 3 == 0:  # Apply to every 3rd product for demo
            original_price = round(price * 1.1, 2)  # 10% higher than current price
            discount_percentage = 10
        
        # Get product categories
        categories = []
        product_categories = db.query(models.ProductToCategory).filter(
            models.ProductToCategory.product_id == product_id
        ).all()
        
        for pc in product_categories:
            category = db.query(models.Category).filter(
                models.Category.category_id == pc.category_id
            ).first()
            
            if category:
                # Get category description for the name
                category_description = db.query(models.CategoryDescription).filter(
                    models.CategoryDescription.category_id == category.category_id,
                    models.CategoryDescription.language_id == 1  # Assuming language_id 1 is default
                ).first()
                
                categories.append({
                    "id": category.category_id,
                    "name": category_description.name if category_description else f"Category {category.category_id}",
                    "searchFilter": f"categoryId={category.category_id}"
                })
        
        # Get additional product images
        more_images = []
        try:
            product_images = db.query(models.ProductImage).filter(
                models.ProductImage.product_id == product_id
            ).order_by(models.ProductImage.sort_order).all()
            
            for img in product_images:
                if img.image:
                    more_images.append(f"https://assets2.panuval.com/image/cache/catalog/{img.image}")
        except:
            # If the model doesn't exist or there's an error, continue without additional images
            pass
        
        # Compile product details
        details = {
            "ISBN": product.isbn,
            "SKU": product.sku,
            "Model": product.model,
            "Manufacturer": str(product.manufacturer_id),
            "Weight": str(product.weight),
            "Height": str(product.height),
            "Width": str(product.width),
            "Length": str(product.length)
        }
        
        # Get authors
        authors = []
        try:
            product_authors = db.query(models.ProductAuthor).filter(
                models.ProductAuthor.product_id == product_id
            ).all()
            
            for pa in product_authors:
                author = db.query(models.Author).filter(
                    models.Author.author_id == pa.author_id,
                    models.Author.status == True
                ).first()
                
                if author:
                    authors.append({
                        "id": author.author_id,
                        "name": author.name,
                        "imageUrl": f"https://assets2.panuval.com/image/cache/catalog/{author.image}" if author.image else None,
                        "searchFilter": f"authorId={author.author_id}"
                    })
        except:
            # If the model doesn't exist or there's an error, continue without authors
            pass
            
        # Get publishers
        publishers = []
        try:
            product_publishers = db.query(models.ProductPublisher).filter(
                models.ProductPublisher.product_id == product_id
            ).all()
            
            for pp in product_publishers:
                publisher = db.query(models.Publisher).filter(
                    models.Publisher.publisher_id == pp.publisher_id,
                    models.Publisher.status == True
                ).first()
                
                if publisher:
                    publishers.append({
                        "id": publisher.publisher_id,
                        "name": publisher.name,
                        "imageUrl": f"https://assets2.panuval.com/image/cache/catalog/{publisher.image}" if publisher.image else None,
                        "searchFilter": f"publisherId={publisher.publisher_id}"
                    })
        except:
            # If the model doesn't exist or there's an error, continue without publishers
            pass
        
        # Get the item_id to return (either one_items.id or fallback to product.product_id)
        response_item_id = item_id  # Use the requested item_id which is already mapped correctly
        
        # Build response
        return {
            "itemId": response_item_id,
            "title": description.name,
            "subTitle": None,  # Assuming no subtitle in current model
            "description": description.description,
            "coverImageUrl": f"https://assets2.panuval.com/image/cache/catalog/{product.image}" if product.image else None,
            "moreImages": more_images,
            "price": price,
            "originalPrice": original_price,
            "discountPercentage": discount_percentage,
            "stockStatus": stock_status,
            "shortDescription": description.meta_description or "",
            "details": details,
            "authors": authors,
            "publishers": publishers,
            "categories": categories,
            "highlights": description.tag.split(',') if description.tag else [],
            "policyText": None,  # Would need policy configuration
            "label": {
                "label": "NEW_ARRIVAL" if (product.date_added and (datetime.now() - product.date_added).days < 30) else None,
                "showLabel": True if (product.date_added and (datetime.now() - product.date_added).days < 30) else False,
                "labelType": "NEW_ARRIVAL" if (product.date_added and (datetime.now() - product.date_added).days < 30) else "NONE"
            }
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving item details: {str(e)}")