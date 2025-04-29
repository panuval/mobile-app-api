from typing import Optional, List, Union, Literal
from datetime import datetime
from pydantic import BaseModel, Field

class SectionMetadata(BaseModel):
    """Schema for section metadata in the home page layout."""
    sectionId: str = Field(..., alias="section_id")
    displayType: Literal["TEXT", "CAROUSEL", "TILE"] = Field(..., alias="display_type")
    contentType: Literal["LABEL", "BANNER", "BOOK", "CATEGORY", "AUTHOR", "PUBLISHER"] = Field(..., alias="content_type")
    title: Optional[str] = None
    showTitle: bool = Field(True, alias="show_title")
    subTitle: Optional[str] = Field(None, alias="sub_title")
    showSubTitle: bool = Field(True, alias="show_sub_title")
    showViewAll: bool = Field(False, alias="show_view_all")
    showName: bool = Field(True, alias="show_name")
    showAuthor: bool = Field(True, alias="show_author")
    order: int
    visible: bool
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class BannerContent(BaseModel):
    """Schema for banner content in a section."""
    name: str
    imageUrl: str = Field(..., alias="image_url")
    linkType: Literal["ITEM", "NONE", "SEARCH_FILTER"] = Field(..., alias="link_type")
    itemId: Optional[int] = Field(None, alias="item_id")
    searchFilter: Optional[str] = Field(None, alias="search_filter")
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class ItemSummary(BaseModel):
    """Schema for product item summary in a section."""
    itemId: int = Field(..., alias="item_id")
    name: str
    imageUrl: Optional[str] = Field(None, alias="image_url")
    price: float
    originalPrice: Optional[float] = Field(None, alias="original_price")
    discountPercentage: Optional[float] = Field(None, alias="discount_percentage")
    stockStatus: Literal["AVAILABLE", "IN_STOCK", "OUT_OF_STOCK", "PRE_ORDER", "OUT_OF_PRINT"] = Field(..., alias="stock_status")
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class AuthorPublisherCategoryInfo(BaseModel):
    """Schema for author, publisher, or category info in a section."""
    name: str
    imageUrl: Optional[str] = Field(None, alias="image_url")
    searchFilter: str = Field(..., alias="search_filter")
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class SectionResponse(BaseModel):
    """Schema for section content response."""
    sectionId: str = Field(..., alias="section_id")
    displayType: Literal["TEXT", "CAROUSEL", "TILE"] = Field(..., alias="display_type")
    contentType: Literal["LABEL", "BANNER", "BOOK", "CATEGORY", "AUTHOR", "PUBLISHER"] = Field(..., alias="content_type")
    title: Optional[str] = None
    showTitle: bool = Field(True, alias="show_title")
    subTitle: Optional[str] = Field(None, alias="sub_title")
    showSubTitle: bool = Field(True, alias="show_sub_title")
    showViewAll: bool = Field(False, alias="show_view_all")
    content: List[Union[ItemSummary, BannerContent, AuthorPublisherCategoryInfo]]
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class StockStatus(BaseModel):
    """Schema for stock status."""
    id: int
    name: str
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class ItemDetail(BaseModel):
    """Schema for detailed item information."""
    itemId: int = Field(..., alias="item_id")
    title: str
    subTitle: Optional[str] = Field(None, alias="subtitle")
    description: str
    coverImageUrl: Optional[str] = Field(None, alias="cover_image_url")
    moreImages: Optional[List[str]] = Field(None, alias="more_images")
    price: float
    originalPrice: Optional[float] = Field(None, alias="original_price")
    discountPercentage: Optional[float] = Field(None, alias="discount_percentage")
    stockStatus: Literal["AVAILABLE", "IN_STOCK", "OUT_OF_STOCK", "PRE_ORDER", "OUT_OF_PRINT"] = Field(..., alias="stock_status")
    shortDescription: str = Field(..., alias="short_description")
    details: Optional[dict] = None
    authors: List[dict] = Field(default_factory=list)
    publishers: List[dict] = Field(default_factory=list)
    categories: List[dict] = Field(default_factory=list)
    highlights: List[str] = Field(default_factory=list)
    policyText: Optional[str] = Field(None, alias="policy_text")
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class ItemSearchResponse(BaseModel):
    """Schema for item search response."""
    displayText: Optional[str] = Field(None, alias="display_text")
    items: List[ItemSummary]
    pagination: dict
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True