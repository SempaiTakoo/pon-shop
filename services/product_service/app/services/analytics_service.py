import redis
from datetime import datetime
from ..config import settings

class AnalyticsService:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)
    
    def track_view(self, product_id: int, user_id: int):
        timestamp = datetime.now().timestamp()
        self.redis.zadd(f"product:views:{product_id}", {user_id: timestamp})
    
    def get_views_count(self, product_id: int):
        return self.redis.zcard(f"product:views:{product_id}")