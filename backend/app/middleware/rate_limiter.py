"""Rate limiting middleware."""
from fastapi import Request, HTTPException, status
from typing import Callable
import time
from app.utils.cache import cache
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Rate limiter using Redis."""
    
    def __init__(self, calls: int = None, period: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            calls: Number of calls allowed per period
            period: Time period in seconds
        """
        self.calls = calls or settings.RATE_LIMIT_PER_MINUTE
        self.period = period
    
    async def __call__(self, request: Request, call_next: Callable):
        """Rate limit middleware."""
        # Get client identifier (IP or user ID)
        client_id = request.client.host
        
        # Check if user is authenticated
        auth_header = request.headers.get("authorization")
        if auth_header:
            # Use user-specific rate limit if authenticated
            client_id = f"user:{auth_header[-10:]}"
        
        # Rate limit key
        rate_key = f"rate_limit:{client_id}"
        
        # Get current count
        current = cache.get(rate_key)
        
        if current is None:
            # First request in this period
            cache.set(rate_key, 1, self.period)
        elif current >= self.calls:
            # Rate limit exceeded
            logger.warning("rate_limit_exceeded", client_id=client_id)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        else:
            # Increment count
            cache.redis_client.incr(rate_key)
        
        response = await call_next(request)
        return response


async def check_rate_limit(request: Request, calls: int = None):
    """Check rate limit for a specific endpoint."""
    calls = calls or settings.RATE_LIMIT_PER_MINUTE
    client_id = request.client.host
    
    rate_key = f"rate_limit:{client_id}:{request.url.path}"
    current = cache.get(rate_key)
    
    if current is None:
        cache.set(rate_key, 1, 60)
    elif current >= calls:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    else:
        cache.redis_client.incr(rate_key)


