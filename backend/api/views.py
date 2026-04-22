from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOrgAdminOrOwner
from .models import User, Organization, Member
from .serializers import UserSerializer, OrganizationSerializer, MemberSerializer
   
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # Apply the strict permission we just created
    permission_classes = [IsAuthenticated, IsOrgAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        
        # Scenario 1: Superuser (See All)
        if user.is_superuser:
            return User.objects.all()
            
        # Scenario 2: Admin (See All in THEIR Org)
        if user.role == 'ADMIN':
            return User.objects.filter(organization=user.organization)
            
        # Scenario 3: Member (See ONLY Self) -> FIXES "Member Viewing Others"
        # This returns a list containing only 1 item (themselves)
        return User.objects.filter(id=user.id)

    def perform_create(self, serializer):
        # FIXES "Admin adding users to other Orgs"
        # We override the save process.
        
        user = self.request.user
        
        if user.is_superuser:
            # Superuser can set organization manually if they want
            serializer.save()
        else:
            # For everyone else (Admins), we FORCE the organization to be their own.
            # Even if they sent "organization": 99 in the JSON, it is ignored here.
            serializer.save(organization=user.organization)

class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsOrgAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Member.objects.all()
        if user.role == 'ADMIN':
            return Member.objects.filter(organization=user.organization)
        return Member.objects.filter(user=user)

    def perform_create(self, serializer):
        # Auto-link to Admin's Organization
        serializer.save(organization=self.request.user.organization)

    # --- THE MAGIC BUTTON ---
    @action(detail=True, methods=['post'])
    def activate_login(self, request, pk=None):
        member = self.get_object()

        if member.user:
            return Response(
                {"error": "User already has a login."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use email from Member profile as the username
        email = member.email
        # Allow Admin to set password, or default to a temp one
        password = request.data.get('password', 'ChangeMe123!') 

        try:
            # 1. Create the User (The Key Card)
            new_user = User.objects.create_user(
                username=email, 
                email=email,
                password=password,
                first_name=member.name,
                role='MEMBER',
                organization=member.organization
            )

            # 2. Link it to the Member (The Folder)
            member.user = new_user
            member.save()

            return Response({
                "status": "Login Activated Successfully", 
                "user_id": new_user.id,
                "username": new_user.username
            })
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrganizationSerializer
    # We can stick to IsAdminOrReadOnly here since members shouldn't create Orgs anyway
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Organization.objects.all()
        return Organization.objects.filter(id=user.organization.id)