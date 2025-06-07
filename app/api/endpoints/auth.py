from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
import logging

from app.schemas.otp import OTPRequest, OTPVerifyRequest, OTPResponse, OTPVerifyResponse
from app.services.msg91_service import OTPManager
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

def get_otp_manager() -> OTPManager:
    """Dependency to get OTP manager instance"""
    return OTPManager(
        auth_key=settings.MSG91_AUTH_KEY,
        template_id=getattr(settings, 'MSG91_TEMPLATE_ID', None)
    )

@router.post("/send-otp", response_model=OTPResponse)
async def send_otp(
    request: OTPRequest,
    otp_manager: OTPManager = Depends(get_otp_manager)
):
    """
    Send OTP to mobile number
    """
    try:
        success, message = otp_manager.request_otp(
            mobile=request.mobile,
            otp_expiry=request.otp_expiry
        )
        
        if success:
            return OTPResponse(
                success=True,
                message=message,
                request_id=otp_manager.pending_otps.get(request.mobile, {}).get('request_id')
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
            
    except Exception as e:
        logger.error(f"Error sending OTP: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP"
        )

@router.post("/verify-otp", response_model=OTPVerifyResponse)
async def verify_otp(
    request: OTPVerifyRequest,
    otp_manager: OTPManager = Depends(get_otp_manager)
):
    """
    Verify OTP for mobile number
    """
    try:
        success, message = otp_manager.verify_otp(
            mobile=request.mobile,
            otp=request.otp
        )
        
        return OTPVerifyResponse(
            success=success,
            message=message,
            verified=success
        )
        
    except Exception as e:
        logger.error(f"Error verifying OTP: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify OTP"
        )