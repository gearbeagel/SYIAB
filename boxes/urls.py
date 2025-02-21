from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

import boxes.views as bxv

router = DefaultRouter()
router.register(r'boxes', bxv.BoxViewSet, basename='box')

urlpatterns = [
    path('create/', bxv.create_a_box, name='create_box'),
    path('boxes/<int:box_id>', bxv.view_box, name='view_box'),
    path('boxes/<int:box_id>/create_memory/', bxv.create_memory, name='create_memory'),
    path('boxes/<int:box_id>/<int:memory_id>/', bxv.view_memory, name='view_memory'),
    path('boxes/<int:box_id>/delete/', bxv.delete_box, name='delete_box'),
    path('boxes/<int:box_id>/<int:memory_id>/delete/', bxv.delete_memory, name='delete_memory'),
    path('boxes/<int:box_id>/lock/', bxv.lock_box, name='lock_box'),
    path('boxes/<int:box_id>/edit/', bxv.edit_box, name='edit_box'),
    path('api/', include(router.urls)),
]
