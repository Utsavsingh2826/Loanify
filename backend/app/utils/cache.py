"""Redis cache management."""
import redis
import json
from typing import Any, Optional
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CacheManager:
    """Redis cache manager."""
    
    def __init__(self):
        """Initialize Redis connection."""
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            decode_responses=True
        )
        logger.info("Redis connection established")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("cache_get_error", key=key, error=str(e))
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL."""
        try:
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
            return True
        except Exception as e:
            logger.error("cache_set_error", key=key, error=str(e))
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error("cache_delete_error", key=key, error=str(e))
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error("cache_exists_error", key=key, error=str(e))
            return False
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get conversation session."""
        return self.get(f"session:{session_id}")
    
    def set_session(self, session_id: str, session_data: dict, ttl: int = 7200) -> bool:
        """Set conversation session."""
        return self.set(f"session:{session_id}", session_data, ttl)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete conversation session."""
        return self.delete(f"session:{session_id}")


# Global cache instance
cache = CacheManager()


