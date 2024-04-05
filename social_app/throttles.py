

from rest_framework.throttling import UserRateThrottle

class FriendRequestThrottle(UserRateThrottle):
    rate = '1/minute'  # Limit to 3 requests per minute
    scope = 'friend_request'  # Unique scope for friend requests
