import http.client
import json
import os
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class OTPStatus(Enum):
    """Enum for OTP operation status"""
    SUCCESS = "success"
    FAILED = "failed"
    INVALID = "invalid"
    EXPIRED = "expired"

@dataclass
class OTPResponse:
    """Data class for OTP response"""
    status: OTPStatus
    message: str
    request_id: Optional[str] = None
    raw_response: Optional[Dict] = None

class MSG91OTPService:
    """
    MSG91 OTP Service for sending and verifying OTPs
    """
    
    def __init__(self, auth_key: str, template_id: Optional[str] = None):
        """
        Initialize MSG91 OTP Service
        
        Args:
            auth_key: Your MSG91 authentication key
            template_id: Optional template ID for OTP messages
        """
        self.auth_key = auth_key
        self.template_id = template_id
        self.base_host = "control.msg91.com"
        
    def send_otp(self, 
                 mobile: str, 
                 otp_expiry: int = 300,
                 real_time_response: bool = True) -> OTPResponse:
        """
        Send OTP to a mobile number
        
        Args:
            mobile: Mobile number with country code (e.g., 919876543210)
            otp_expiry: OTP expiry time in seconds (default: 300 seconds)
            real_time_response: Whether to get real-time response
            
        Returns:
            OTPResponse object with status and details
        """
        try:
            conn = http.client.HTTPSConnection(self.base_host)
            
            payload_data = {
                "mobile": mobile,
                "authkey": self.auth_key,
                "otp_expiry": str(otp_expiry),
                "realTimeResponse": "1" if real_time_response else "0"
            }
            
            if self.template_id:
                payload_data["template_id"] = self.template_id
            
            payload = json.dumps(payload_data)
            
            headers = {
                'Content-Type': "application/json",
                'content-type': "application/json"
            }
            
            url_params = f"?otp_expiry={otp_expiry}&mobile={mobile}&authkey={self.auth_key}&realTimeResponse={'1' if real_time_response else '0'}"
            if self.template_id:
                url_params += f"&template_id={self.template_id}"
                
            conn.request("POST", f"/api/v5/otp{url_params}", payload, headers)
            
            res = conn.getresponse()
            data = res.read()
            response_text = data.decode("utf-8")
            
            logger.info(f"Send OTP Response: {response_text}")
            
            try:
                response_json = json.loads(response_text)
                if res.status == 200:
                    return OTPResponse(
                        status=OTPStatus.SUCCESS,
                        message="OTP sent successfully",
                        request_id=response_json.get("request_id"),
                        raw_response=response_json
                    )
                else:
                    return OTPResponse(
                        status=OTPStatus.FAILED,
                        message=response_json.get("message", "Failed to send OTP"),
                        raw_response=response_json
                    )
            except json.JSONDecodeError:
                return OTPResponse(
                    status=OTPStatus.FAILED,
                    message=f"Invalid response format: {response_text}",
                    raw_response={"raw": response_text}
                )
                
        except Exception as e:
            logger.error(f"Error sending OTP: {str(e)}")
            return OTPResponse(
                status=OTPStatus.FAILED,
                message=f"Error sending OTP: {str(e)}"
            )
        finally:
            conn.close()
    
    def verify_otp(self, mobile: str, otp: str) -> OTPResponse:
        """
        Verify OTP for a mobile number
        
        Args:
            mobile: Mobile number with country code
            otp: OTP to verify
            
        Returns:
            OTPResponse object with verification status
        """
        try:
            conn = http.client.HTTPSConnection(self.base_host)
            
            headers = {
                'authkey': self.auth_key
            }
            
            url = f"/api/v5/otp/verify?otp={otp}&mobile={mobile}"
            conn.request("GET", url, headers=headers)
            
            res = conn.getresponse()
            data = res.read()
            response_text = data.decode("utf-8")
            
            logger.info(f"Verify OTP Response: {response_text}")
            
            try:
                response_json = json.loads(response_text)
                
                if res.status == 200:
                    if response_json.get("type") == "success":
                        return OTPResponse(
                            status=OTPStatus.SUCCESS,
                            message="OTP verified successfully",
                            raw_response=response_json
                        )
                    else:
                        return OTPResponse(
                            status=OTPStatus.INVALID,
                            message=response_json.get("message", "Invalid OTP"),
                            raw_response=response_json
                        )
                else:
                    return OTPResponse(
                        status=OTPStatus.FAILED,
                        message=response_json.get("message", "OTP verification failed"),
                        raw_response=response_json
                    )
                    
            except json.JSONDecodeError:
                return OTPResponse(
                    status=OTPStatus.FAILED,
                    message=f"Invalid response format: {response_text}",
                    raw_response={"raw": response_text}
                )
                
        except Exception as e:
            logger.error(f"Error verifying OTP: {str(e)}")
            return OTPResponse(
                status=OTPStatus.FAILED,
                message=f"Error verifying OTP: {str(e)}"
            )
        finally:
            conn.close()

class OTPManager:
    """
    High-level OTP Manager for easier usage
    """
    
    def __init__(self, auth_key: str, template_id: Optional[str] = None):
        self.service = MSG91OTPService(auth_key, template_id)
        self.pending_otps = {}
    
    def request_otp(self, mobile: str, otp_expiry: int = 300) -> Tuple[bool, str]:
        """
        Request OTP for a mobile number
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        response = self.service.send_otp(mobile, otp_expiry)
        
        if response.status == OTPStatus.SUCCESS:
            self.pending_otps[mobile] = {
                'request_id': response.request_id,
                'status': 'pending'
            }
            return True, "OTP sent successfully"
        else:
            return False, response.message
    
    def verify_otp(self, mobile: str, otp: str) -> Tuple[bool, str]:
        """
        Verify OTP for a mobile number
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        response = self.service.verify_otp(mobile, otp)
        
        if response.status == OTPStatus.SUCCESS:
            # Update local state if mobile exists in pending_otps
            if mobile in self.pending_otps:
                self.pending_otps[mobile]['status'] = 'verified'
            return True, "OTP verified successfully"
        else:
            return False, response.message