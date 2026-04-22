from rest_framework import serializers
from .models import User, Member, Organization

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'name', 'is_active']

class MemberSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = Member
        fields = [
            'id', 
            'name',           # <--- Input this now
            'email',          # <--- Input this now
            'phone_number', 
            'member_type', 
            'mailing_address', 
            'job',
            'organization_name',
            'user'            # Keep for viewing, but locked for editing
        ]
        # HIDE THE DROPDOWN: Admin cannot manually pick a user.
        extra_kwargs = {
            'user': {'read_only': True} 
        }
        
class UserSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True, default=None)
    password = serializers.CharField(write_only=True)
    member_id = serializers.PrimaryKeyRelatedField(source='member_profile', read_only=True)
    # display = serializers.SerializerMethodField() #default for Allauth

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'organization', 'organization_name', 'password',
            'member_id', 'is_active'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        
        if request and request.user.is_authenticated:
            # LOGIC A: Organization Field
            # ONLY Superusers can manually select an Organization.
            # For Admins/Members, it is auto-assigned, so we lock the field UI.
            if not request.user.is_superuser:
                self.fields['organization'].read_only = True

            # LOGIC B: Role Field
            # Members cannot change their own Role (Promote to Admin).
            # Admins CAN change roles (e.g. create a new Member user).
            if request.user.role == 'MEMBER':
                 self.fields['role'].read_only = True

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user