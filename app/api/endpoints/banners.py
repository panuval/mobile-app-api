from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

# Static banner data
BANNERS = [
    {
        "bannerId": 1,
        "name": "S. Ramakrishnan Books",
        "imageUrl": "https://assets2.panuval.com/image/cache/catalog/0001_WritersPosters/S.Ramakrishnan%20Books-300x300.jpg",
        "linkType": "SEARCH_FILTER",
        "itemId": None,
        "searchFilter": "authorId=123",
        "dateAdded": datetime.now().isoformat()
    },
    {
        "bannerId": 2,
        "name": "Periyar Books",
        "imageUrl": "https://assets2.panuval.com/image/cache/catalog/0001_WritersPosters/Periyar%20Books-300x300.jpg",
        "linkType": "SEARCH_FILTER",
        "itemId": None,
        "searchFilter": "authorId=456",
        "dateAdded": datetime.now().isoformat()
    },
    {
        "bannerId": 3,
        "name": "Balakumaran Books",
        "imageUrl": "https://assets2.panuval.com/image/cache/catalog/0001_WritersPosters/Balakumaran%20Books-300x300.jpg",
        "linkType": "SEARCH_FILTER",
        "itemId": None,
        "searchFilter": "authorId=789",
        "dateAdded": datetime.now().isoformat()
    },
    {
        "bannerId": 4,
        "name": "Jeyamohan Books",
        "imageUrl": "https://assets2.panuval.com/image/cache/catalog/0001_WritersPosters/Jeyamohan%20Books-300x300.jpg",
        "linkType": "SEARCH_FILTER",
        "itemId": None,
        "searchFilter": "authorId=101",
        "dateAdded": datetime.now().isoformat()
    },
    {
        "bannerId": 5,
        "name": "Tolstoy Books",
        "imageUrl": "https://assets2.panuval.com/image/cache/catalog/0001_WritersPosters/Tolstoy%20Books-300x300.jpg",
        "linkType": "SEARCH_FILTER",
        "itemId": None,
        "searchFilter": "authorId=202",
        "dateAdded": datetime.now().isoformat()
    }
]

@router.get("/")
def get_all_banners() -> Any:
    """
    Retrieve all active banners
    """
    return BANNERS

@router.get("/{banner_id}")
def get_banner_by_id(banner_id: int) -> Any:
    """
    Get a specific banner by ID
    """
    for banner in BANNERS:
        if banner["bannerId"] == banner_id:
            return banner
            
    raise HTTPException(status_code=404, detail="Banner not found")