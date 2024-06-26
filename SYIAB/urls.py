"""
URL configuration for SYIAB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

import registration.views
from SYIAB import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registration.views.home, name='home'),
    path('', include('registration.urls')),
    path('', include('boxes.urls')),
    path('', include('profilepage.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
