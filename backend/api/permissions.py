from rest_framework import permissions

class IsOrgAdminOrOwner(permissions.BasePermission):
    """
    STRICT Permission Logic:
    1. Superuser: Can do anything.
    2. Admin: Can do anything (List, Create, Edit, Delete) but logic is restricted to their Org.
    3. Member: 
       - Can List/Retrieve (GET): YES (Filtered to self in views).
       - Can Update (PUT/PATCH): YES (Filtered to self in views).
       - Can Create (POST): NO.
       - Can Delete (DELETE): NO.
    """
    def has_permission(self, request, view):
        # 1. Superuser: Allowed
        if request.user.is_superuser:
            return True

        # 2. Admin: Allowed to access endpoints (Scope restricted by QuerySet)
        if request.user.role == 'ADMIN':
            return True
            
        # 3. Member: Restricted Methods
        if request.user.role == 'MEMBER':
            if request.method in ['POST', 'DELETE']:
                return False # Members cannot Create Users or Delete Users
            return True
            
        return False

    def has_object_permission(self, request, view, obj):
        # Double-check object ownership just in case
        if request.user.is_superuser:
            return True

        # 1. Isolation Rule: No one can touch objects outside their Organization
        if obj.organization != request.user.organization:
            return False

        # 2. Admin: Can touch any object in their Org
        if request.user.role == 'ADMIN':
            return True

        # 3. Member: Can ONLY touch THEMSELVES
        if request.user.role == 'MEMBER':
            return obj.id == request.user.id
            
        return False