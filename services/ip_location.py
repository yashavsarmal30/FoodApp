import ipapi
import time
from typing import Optional, Dict
import logging

class IPLocationService:
    def __init__(self):
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum time between requests in seconds
        self.cache: Dict[str, str] = {}
        self.logger = logging.getLogger(__name__)

    def get_location(self) -> str:
        """Get the user's location with rate limiting and fallback."""
        try:
            current_time = time.time()
            if current_time - self.last_request_time < self.min_request_interval:
                time.sleep(self.min_request_interval - (current_time - self.last_request_time))

            city = self._get_cached_or_fetch('city')
            region = self._get_cached_or_fetch('region')
            
            if city and region:
                return f"📍 {city}, {region}"
            elif city:
                return f"📍 {city}"
            else:
                return "📍 Unknown Location"
                
        except Exception as e:
            self.logger.error(f"Error getting location: {str(e)}")
            return "📍 Unknown Location"

    def _get_cached_or_fetch(self, field: str) -> Optional[str]:
        """Get location data from cache or fetch it with rate limiting."""
        if field in self.cache:
            return self.cache[field]

        try:
            self.last_request_time = time.time()
            result = ipapi.location(output=field)
            self.cache[field] = result
            return result
        except ipapi.exceptions.RateLimited:
            self.logger.warning("IP API rate limit reached")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching {field}: {str(e)}")
            return None

# Create a singleton instance
ip_location_service = IPLocationService() 