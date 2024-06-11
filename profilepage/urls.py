from django.conf.urls.static import static
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

import profilepage.views as pfv
from SYIAB import settings

# DRF Router
router = DefaultRouter()
router.register(r'profile', pfv.ProfileViewSet, basename='profile')

urlpatterns = [
    path('profile/<str:username>/', pfv.view_profile, name='view_profile'),
    path('profile/<str:username>/edit/', pfv.edit_profile, name='edit_profile'),
    path('profile/<str:username>/delete/', pfv.delete_profile, name='delete_profile'),
    path('api/', include(router.urls)),
]