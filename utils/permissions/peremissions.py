from rest_framework.permissions import BasePermission


# 表示登录过，但是不管是否激活
from apps.user.management.permission import PermissionType, Permission
from apps.user.models import UserVip


class LoginAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


# #表示登录过，但未激活了账户
class UnActiveAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_active)


# #表示登录过，而且激活了账户
class ActiveAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)


# 表示未登录
class UnLoginAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)

#VIP
class VipPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(perm=Permission.Role_vip_u,obj={'type':PermissionType.upload})
#Admin
class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(perm=Permission.Role_admin_u,obj={'type':PermissionType.upload})