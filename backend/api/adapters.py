from allauth.headless.adapter import DefaultHeadlessAdapter
from .serializers import UserSerializer 

class CustomHeadlessAdapter(DefaultHeadlessAdapter):
    def serialize_user(self, user):
        # 1. Get the default data (email, id, has_usable_password, etc.)
        data = super().serialize_user(user)

        # 2. Append YOUR custom fields
        data['role'] = user.role
        data['organization'] = user.organization.id if user.organization else None
        data['is_active'] = user.is_active
        
        # Optional: You can also use your DRF serializer here if you prefer
        # return UserSerializer(user).data
        
        return data