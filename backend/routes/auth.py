"""
Authentication Routes
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import logging

from database.postgres import create_user, get_user_by_email, get_user_profile
from services.auth_service import auth_service

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# Request/Response Models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    software_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    hardware_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    robotics_knowledge: bool = False
    learning_goals: Optional[str] = None

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str

class UserProfile(BaseModel):
    user_id: str
    email: str
    software_level: str
    hardware_level: str
    robotics_knowledge: bool
    learning_goals: Optional[str]

# Dependency to get current user from token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = auth_service.decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    return user_id

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """
    Register a new user with profile information
    """
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        password_hash = auth_service.hash_password(request.password)
        
        # Create user profile data
        profile_data = {
            'software_level': request.software_level,
            'hardware_level': request.hardware_level,
            'robotics_knowledge': request.robotics_knowledge,
            'learning_goals': request.learning_goals
        }
        
        # Create user
        user_id = await create_user(request.email, password_hash, profile_data)
        
        # Create access token
        access_token = auth_service.create_access_token(
            data={"sub": user_id, "email": request.email}
        )
        
        logger.info(f"New user registered: {request.email}")
        
        return AuthResponse(
            access_token=access_token,
            user_id=user_id,
            email=request.email
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/signin", response_model=AuthResponse)
async def signin(request: SigninRequest):
    """
    Sign in existing user
    """
    try:
        # Get user
        user = await get_user_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not auth_service.verify_password(request.password, user['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create access token
        access_token = auth_service.create_access_token(
            data={"sub": str(user['id']), "email": user['email']}
        )
        
        logger.info(f"User signed in: {request.email}")
        
        return AuthResponse(
            access_token=access_token,
            user_id=str(user['id']),
            email=user['email']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signin error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sign in failed"
        )

@router.get("/profile", response_model=UserProfile)
async def get_profile(user_id: str = Depends(get_current_user)):
    """
    Get current user's profile
    """
    try:
        # Get user
        user = await get_user_by_email(user_id)  # This should use user_id
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get profile
        profile = await get_user_profile(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        return UserProfile(
            user_id=user_id,
            email=user['email'],
            software_level=profile.get('software_level', 'intermediate'),
            hardware_level=profile.get('hardware_level', 'beginner'),
            robotics_knowledge=profile.get('robotics_knowledge', False),
            learning_goals=profile.get('learning_goals')
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get profile"
        )

@router.post("/verify")
async def verify_token(user_id: str = Depends(get_current_user)):
    """
    Verify if token is valid
    """
    return {"valid": True, "user_id": user_id}