from fastapi import Request, HTTPException
from services.auth_service import auth_service

async def auth_middleware(request: Request, call_next):
    # Skip auth for public endpoints
    public_paths = ["/", "/health", "/docs", "/openapi.json"]
    
    if request.url.path in public_paths:
        return await call_next(request)
    
    # Implement auth logic as needed
    response = await call_next(request)
    return response