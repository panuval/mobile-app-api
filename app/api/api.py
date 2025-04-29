from fastapi import APIRouter

from app.api.endpoints import users, products, cart, orders, banners, offers, campaigns, reviews, promotions, home, items

api_router = APIRouter()

# Authentication routes
api_router.include_router(users.router, prefix="", tags=["authentication"])

# Product management
api_router.include_router(products.router, prefix="/products", tags=["products"])

# Cart management
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])

# Orders and checkout
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(orders.router, prefix="/checkout", tags=["checkout"])

# Home page and layout
api_router.include_router(home.router, prefix="/app/home", tags=["home"])

# Items/Products search and details
api_router.include_router(items.router, prefix="/items", tags=["items"])

# Marketing related routes
api_router.include_router(banners.router, prefix="/banners", tags=["banners"])
api_router.include_router(offers.router, prefix="/offers", tags=["offers"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(promotions.router, prefix="/promotions", tags=["promotions"])