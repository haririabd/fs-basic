from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    """
    Support Multi-tenancy and Roles.
    """
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        ADMIN = "ADMIN", "Admin"
        MEMBER = "MEMBER", "Member"

    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name="users",
        null=True, blank=True # Nullable for superusers/platform owners
    )
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.MEMBER)
    
class Member(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    class MemberType(models.TextChoices):
        LIFETIME = "LIFETIME", "Lifetime"
        NORMAL = "NORMAL", "Normal"

    # LINK IS NOW OPTIONAL (For offline members)
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='member_profile'
    )
    
    membership_number = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=255, help_text="Full Name")
    email = models.EmailField(help_text="Contact Email")
    phone_number = models.CharField(max_length=20, blank=True)
    member_type = models.CharField(max_length=20, choices=MemberType.choices, default=MemberType.LIFETIME, verbose_name="Member Type")

    job = models.CharField(max_length=255, blank=True)
    mailing_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.membership_number} ({self.name})"