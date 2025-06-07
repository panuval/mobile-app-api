from pydantic import BaseModel, Field
from typing import Optional

class OTPRequest(BaseModel):
    mobile: str = Field(..., description="Mobile number with country code (e.g., 919876543210)")
    otp_expiry: Optional[int] = Field(300, description="OTP expiry time in seconds", ge=60, le=600)

class OTPVerifyRequest(BaseModel):
    mobile: str = Field(..., description="Mobile number with country code")
    otp: str = Field(..., description="OTP code to verify", min_length=4, max_length=8)

class OTPResponse(BaseModel):
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

class OTPVerifyResponse(BaseModel):
    success: bool = Field(..., description="Whether OTP verification was successful")
    message: str = Field(..., description="Verification result message")
    verified: bool = Field(..., description="Whether the OTP was verified successfully")