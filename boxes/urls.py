from django.conf.urls.static import static
from django.urls import path
import boxes.views
from SYIAB import settings

urlpatterns = [
    path('create/', boxes.views.create_a_box, name='create'),
    path('boxes/<int:box_id>', boxes.views.view_box, name='view_box'),
    path('boxes/<int:box_id>/create_memory/', boxes.views.create_memory, name='create_memory'),
    path('boxes/<int:box_id>/<int:memory_id>/', boxes.views.view_memory, name='view_memory'),
    path('boxes/<int:box_id>/delete/', boxes.views.delete_box, name='delete_box'),
    path('boxes/<int:box_id>/<int:memory_id>/delete/', boxes.views.delete_memory, name='delete_memory'),
    path('boxes/<int:box_id>/lock/', boxes.views.lock_box, name='lock_box'),
    path('boxes/<int:box_id>/edit/', boxes.views.edit_box, name='edit_box'),
]
