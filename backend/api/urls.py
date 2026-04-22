from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OrganizationViewSet, MemberViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'members', MemberViewSet, basename='member')

urlpatterns = [
    path('', include(router.urls)),
    path('_allauth/', include('allauth.headless.urls')),
]