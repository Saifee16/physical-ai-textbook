from fastapi import Request, HTTPException
from collections import defaultdict
import time

# Simple in-memory rate limiter
request_counts = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    # Remove old requests (older than 1 minute)
    request_counts[client_ip] = [
        t for t in request_counts[client_ip] 
        if current_time - t < 60
    ]
    
    # Check if limit exceeded (100 requests per minute)
    if len(request_counts[client_ip]) >= 100:
        raise HTTPException(status_code=429, detail="Too many requests")
    
    request_counts[client_ip].append(current_time)
    
    response = await call_next(request)
    return response