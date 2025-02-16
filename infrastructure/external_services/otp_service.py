# infrastructure/external_services/otp_service.py

import random
import redis
from django.conf import settings

# Configure the Redis client using settings (set REDIS_HOST, REDIS_PORT, and REDIS_DB in your settings.py)
redis_client = redis.Redis(
    host=getattr(settings, 'REDIS_HOST', 'localhost'),
    port=getattr(settings, 'REDIS_PORT', 6379),
    db=getattr(settings, 'REDIS_DB', 0),
)

def generate_otp(email, ttl=300):
    """
    Generate a 6-digit OTP, store it in Redis with a TTL (default: 5 minutes), and return it.
    """
    otp = str(random.randint(100000, 999999))
    key = f"otp:{email}"
    redis_client.set(key, otp, ex=ttl)
    return otp

def validate_otp(email, input_otp):
    """
    Validate the OTP for the given email. If valid, delete it from Redis.
    """
    key = f"otp:{email}"
    stored = redis_client.get(key)
    if stored is None:
        return False
    stored = stored.decode("utf-8")
    if stored == input_otp:
        redis_client.delete(key)
        return True
    return False
