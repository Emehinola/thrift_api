from rest_framework.permissions import BasePermission
from .exceptions import UnauthorizedException, AdminAccessOnly
from rest_framework import status

safe_methods = ['GET', 'HEAD', 'OPTIONS']

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if (request.method in safe_methods) or request.user.is_admin:
            return True
        
        raise AdminAccessOnly()
        
    
class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if (request.method in safe_methods) or request.user.is_authenticated:
            return True
        
        raise UnauthorizedException()
    
class IsStrictlyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
        raise UnauthorizedException()