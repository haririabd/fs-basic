from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Organization, User, Member

# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    
admin.site.register(Organization, OrganizationAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number", "member_type")
    
admin.site.register(Member, MemberAdmin)

# 1. Configuration for your Custom User
class UserAdmin(BaseUserAdmin):
    # Columns to show in the list
    list_display = ('username', 'email', 'role', 'organization', 'is_active')
    
    # Filters on the right side
    list_filter = ('role', 'organization', 'is_active')
    
    # Configuration to allow editing custom fields (Role/Org) in the detailed view
    # We append our custom fields to the standard User fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('SaaS Info', {'fields': ('organization', 'role')}),
    )
    
    # Also add them to the "Add User" form
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('SaaS Info', {'fields': ('organization', 'role')}),
    )
    
admin.site.register(User, UserAdmin)
    