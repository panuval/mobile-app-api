from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    firstname: str
    lastname: str
    password: str
    email: EmailStr
    

class UserLogin(BaseModel):
    username: str  # Can be username or email
    password: str

class User(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int = None