from rest_framework import permissions
from apps.affiliate.models import PaymentChoice
from apps.entity.models import Entity, DirectoratePosition

class IsUserEntity(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, DirectoratePosition):
            if request.user.entity == obj.entity:
                return True

class EntityAdminPermission(permissions.BasePermission):
    """
    Global permission for check if the current user pertains to the object entity and is admin
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Entity):
            if request.user.entity == obj and request.user.is_entity_admin:
                return True
        else:
            if request.user.entity == obj.entity and request.user.is_entity_admin:
                return True
        return False
        
    
class IsUserOwner(permissions.BasePermission):
    """
    Global permission for check if the current user owns the object
    If current user is entity admin, always returns True
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, PaymentChoice):
            if request.user.affiliate == obj.affiliate:
                return True
        if request.user.entity == obj.entity and request.user.is_entity_admin:
            return True
        return False
    
