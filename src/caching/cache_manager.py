import logging
from typing import Any, Optional, Dict
import time

logger = logging.getLogger(__name__)

class CacheManager:
    """
    Manages the cache for storing results of expensive operations (e.g., parsing, LLM calls).
    
    Uses an in-memory dictionary as a placeholder for a real cache like Redis or Memcached.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        # In-memory store: {key: {"value": Any, "expiry": int}}
        self._cache: Dict[str, Dict[str, Any]] = {}
        logger.info("CacheManager initialized. Using in-memory cache.")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from the cache. Returns None if key is not found or has expired.
        """
        if key not in self._cache:
            return None
        
        item = self._cache[key]
        
        # Проверка на истечение срока действия (Expiry check)
        if item.get("expiry") is not None and item["expiry"] < time.time():
            logger.debug(f"Cache miss: Key {key} expired.")
            del self._cache[key]
            return None
        
        logger.debug(f"Cache hit: Key {key}.")
        return item["value"]

    def set(self, key: str, value: Any, ttl: Optional[int] = 3600) -> None:
        """
        Stores a value in the cache with an optional Time-To-Live (TTL) in seconds.
        По умолчанию TTL = 1 час (3600 секунд).
        """
        expiry = time.time() + ttl if ttl is not None else None
        self._cache[key] = {
            "value": value,
            "expiry": expiry
        }
        logger.debug(f"Cache set: Key {key} with TTL {ttl}.")

    def delete(self, key: str) -> None:
        """
        Deletes a key from the cache.
        """
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache deleted: Key {key}.")

    def clear(self) -> None:
        """
        Clears the entire cache.
        """
        self._cache = {}
        logger.info("Cache cleared.")

if __name__ == "__main__":
    # Пример использования (Example usage)
    manager = CacheManager({})
    
    # Установка значения с TTL
    manager.set("test_key", "cached_value", ttl=1)
    
    # Получение значения (Cache hit)
    value1 = manager.get("test_key")
    print(f"Value 1: {value1}")
    
    # Ожидание истечения TTL
    print("Waiting for 1.1 seconds...")
    time.sleep(1.1)
    
    # Получение значения (Cache miss - expired)
    value2 = manager.get("test_key")
    print(f"Value 2 (after expiry): {value2}")
    
    # Установка значения без TTL
    manager.set("permanent_key", "always_here", ttl=None)
    value3 = manager.get("permanent_key")
    print(f"Value 3: {value3}")
    
    manager.delete("permanent_key")
    value4 = manager.get("permanent_key")
    print(f"Value 4 (after delete): {value4}")

