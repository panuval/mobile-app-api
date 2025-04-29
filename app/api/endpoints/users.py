from datetime import timedelta
from typing import Any
import hashlib
from sqlalchemy.sql import func

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, models
from app.core import security
from app.core.opencart_security import verify_opencart_password  # Import the function
from app.core.config import settings
from app.db.database import get_db

router = APIRouter()

@router.post("/login", response_model=dict)
def login(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        # Find the user by username
        user = db.query(models.User).filter(models.User.username == form_data.username).first()
        
        if not user:
            # Try finding by email as fallback
            user = db.query(models.User).filter(models.User.email == form_data.username).first()
            
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password using OpenCart's method (SHA-1 with separate salt)
        if not verify_opencart_password(form_data.password, user.password, user.salt):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.user_id, expires_delta=access_token_expires
        )
        
        return {
            "status": "success",
            "data": {
                "token": access_token,
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email
            }
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.post("/register", response_model=dict)
def register_user(
    user_in: schemas.UserCreate, 
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user
    """
    try:
        # Check if user exists
        existing_user = db.query(models.User).filter(
            (models.User.username == user_in.username) | 
            (models.User.email == user_in.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered",
            )
        
        # Generate salt
        salt = security.generate_salt()
        
        # Generate password hash
        hashed_password = hashlib.sha1((salt + user_in.password).encode()).hexdigest()
        
        # Create new user
        new_user = models.User(
            user_group_id=1,  # Default user group
            username=user_in.username,
            password=hashed_password,
            salt=salt,
            firstname=user_in.firstname,
            lastname=user_in.lastname,
            email=user_in.email,
            image="",
            code="",
            ip="127.0.0.1",  # Default IP
            status=1,  # Active
            date_added=func.now()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "status": "success",
            "data": {
                "user_id": new_user.user_id,
                "username": new_user.username
            }
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )