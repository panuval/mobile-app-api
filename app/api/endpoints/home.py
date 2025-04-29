from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas
from app.db.database import get_db
from app.schemas.layout import SectionMetadata, SectionResponse

router = APIRouter()

@router.get("/layout")
def get_home_layout(
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve the home page layout structure.
    Returns metadata (type, order, visibility, ID) for sections to be displayed on the home page.
    """
    try:
        # Return mock data until tables are created
        result = [
            {
                "sectionId": "1",
                "displayType": "CAROUSEL",
                "contentType": "BANNER",
                "title": "Featured Banners",
                "showTitle": True,
                "subTitle": "Explore our collections",
                "showSubTitle": True,
                "showViewAll": False,
                "showName": True,
                "showAuthor": True,
                "order": 1,
                "visible": True
            },
            {
                "sectionId": "2",
                "displayType": "CAROUSEL",
                "contentType": "BOOK",
                "title": "New Arrivals",
                "showTitle": True,
                "subTitle": "Latest books",
                "showSubTitle": True,
                "showViewAll": True,
                "showName": True,
                "showAuthor": True,
                "order": 2,
                "visible": True
            },
            {
                "sectionId": "3",
                "displayType": "TILE",
                "contentType": "CATEGORY",
                "title": "Browse Categories",
                "showTitle": True,
                "subTitle": "Find your interest",
                "showSubTitle": False,
                "showViewAll": False,
                "showName": True,
                "showAuthor": False,
                "order": 3,
                "visible": True
            }
        ]
        return result
        
        # Map database objects to response schema
        result = []
        for section in sections:
            result.append({
                "sectionId": str(section.section_id),
                "displayType": section.display_type,
                "contentType": section.content_type,
                "title": section.title,
                "showTitle": section.show_title,
                "subTitle": section.sub_title,
                "showSubTitle": section.show_sub_title,
                "showViewAll": section.show_view_all,
                "showName": section.show_name,
                "showAuthor": section.show_author,
                "order": section.order_sort,
                "visible": section.visible
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving home layout: {str(e)}")

@router.get("/section/{section_id}")
def get_section_content(
    section_id: str = Path(..., description="The ID of the section to retrieve"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve detailed content for a specific home page section by ID.
    The response structure varies based on the section's content type.
    """
    try:
        # Return mock data based on section_id
        mock_sections = {
            "1": {
                "sectionId": "1",
                "displayType": "CAROUSEL",
                "contentType": "BANNER",
                "title": "Featured Banners",
                "showTitle": True,
                "subTitle": "Explore our collections",
                "showSubTitle": True,
                "showViewAll": False,
                "content": []
            },
            "2": {
                "sectionId": "2",
                "displayType": "CAROUSEL",
                "contentType": "BOOK",
                "title": "New Arrivals",
                "showTitle": True,
                "subTitle": "Latest books",
                "showSubTitle": True,
                "showViewAll": True,
                "content": []
            },
            "3": {
                "sectionId": "3",
                "displayType": "TILE",
                "contentType": "CATEGORY",
                "title": "Browse Categories",
                "showTitle": True,
                "subTitle": "Find your interest",
                "showSubTitle": False,
                "showViewAll": False,
                "content": []
            }
        }
        
        if section_id not in mock_sections:
            raise HTTPException(status_code=404, detail="Section not found")
            
        response = mock_sections[section_id]
        
        # Skip querying content items since we're using mock data
        
        # Add mock content based on section id
        if response["sectionId"] == "1":
            # Add mock banner content
            response["content"] = [
                {
                    "name": "Summer Sale",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/banners/summer_sale.jpg",
                    "linkType": "SEARCH_FILTER",
                    "itemId": None,
                    "searchFilter": "discounted=true"
                },
                {
                    "name": "New Arrivals",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/banners/new_arrival.jpg",
                    "linkType": "SEARCH_FILTER",
                    "itemId": None,
                    "searchFilter": "sort=newest"
                }
            ]
        elif response["sectionId"] == "2":
            # Add mock book content
            response["content"] = [
                {
                    "itemId": 10027453,
                    "name": "Cooking with Love",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/products/cooking_love.jpg",
                    "price": 29.99,
                    "originalPrice": 39.99,
                    "discountPercentage": 25,
                    "stockStatus": "IN_STOCK"
                },
                {
                    "itemId": 10027454,
                    "name": "History of AI",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/products/history_ai.jpg",
                    "price": 25.99,
                    "originalPrice": 25.99,
                    "discountPercentage": None,
                    "stockStatus": "IN_STOCK"
                }
            ]
        elif response["sectionId"] == "3":
            # Add mock category content
            response["content"] = [
                {
                    "name": "Fiction",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/fiction.jpg",
                    "searchFilter": "categoryId=1"
                },
                {
                    "name": "Non-Fiction",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/non_fiction.jpg",
                    "searchFilter": "categoryId=2"
                },
                {
                    "name": "Academic",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/academic.jpg",
                    "searchFilter": "categoryId=3"
                },
                {
                    "name": "Children's",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/children.jpg",
                    "searchFilter": "categoryId=4"
                },
                {
                    "name": "Biography",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/biography.jpg",
                    "searchFilter": "categoryId=5"
                },
                {
                    "name": "Science Fiction",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/sci_fi.jpg",
                    "searchFilter": "categoryId=6"
                },
                {
                    "name": "Mystery",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/mystery.jpg",
                    "searchFilter": "categoryId=7"
                },
                {
                    "name": "Romance",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/romance.jpg",
                    "searchFilter": "categoryId=8"
                },
                {
                    "name": "Fantasy",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/fantasy.jpg",
                    "searchFilter": "categoryId=9"
                },
                {
                    "name": "History",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/history.jpg",
                    "searchFilter": "categoryId=10"
                },
                {
                    "name": "Self-Help",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/self_help.jpg",
                    "searchFilter": "categoryId=11"
                },
                {
                    "name": "Business",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/business.jpg",
                    "searchFilter": "categoryId=12"
                },
                {
                    "name": "Health",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/health.jpg",
                    "searchFilter": "categoryId=13"
                },
                {
                    "name": "Travel",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/travel.jpg",
                    "searchFilter": "categoryId=14"
                },
                {
                    "name": "Cooking",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/cooking.jpg",
                    "searchFilter": "categoryId=15"
                },
                {
                    "name": "Art & Photography",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/art_photography.jpg",
                    "searchFilter": "categoryId=16"
                },
                {
                    "name": "Religion",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/religion.jpg",
                    "searchFilter": "categoryId=17"
                },
                {
                    "name": "Science",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/science.jpg",
                    "searchFilter": "categoryId=18"
                },
                {
                    "name": "Technology",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/technology.jpg",
                    "searchFilter": "categoryId=19"
                },
                {
                    "name": "Poetry",
                    "imageUrl": "https://assets2.panuval.com/image/cache/catalog/categories/poetry.jpg",
                    "searchFilter": "categoryId=20"
                }
            ]
        
        return response
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving section content: {str(e)}")