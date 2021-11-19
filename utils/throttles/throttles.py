# 匿名用户频率限制
from rest_framework.throttling import SimpleRateThrottle


class LuffyAnonRateThrottle(SimpleRateThrottle):
    """
    匿名用户，根据IP进行限制
    """
    scope = "luffy_anon"

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


# user用户频率限制
class LuffyUserRateThrottle(SimpleRateThrottle):
    """
    登录用户，根据用户token限制
    """
    scope = "luffy_user"

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        ident = request.user.pk
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
