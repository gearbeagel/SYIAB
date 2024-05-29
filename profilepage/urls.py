from django.conf.urls.static import static
from django.urls import path
import profilepage.views
from SYIAB import settings

urlpatterns = [
    path('<str:username>/', profilepage.views.view_profile, name='view_profile'),
    path('<str:username>/edit', profilepage.views.edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
