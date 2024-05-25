from django.urls import path
import boxes.views

urlpatterns = [
    path('create/', boxes.views.create_a_box, name='create'),
    path('boxes/<int:id>', boxes.views.view_box, name='view'),
]