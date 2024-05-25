from django.urls import path
import registration.views

urlpatterns = [
    path('register/', registration.views.registration_view, name='registration'),
    path('logout/', registration.views.logout_view, name='logout'),
]