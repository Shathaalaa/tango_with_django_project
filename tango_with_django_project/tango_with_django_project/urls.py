"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include
from rango import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rango/', include('rango.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #static is a helper function, it creates a URL pattern that maps
# media URL --> media root on disk, we didn't need that for static files because static files are part from the project so django knows
# how to get to them and it automatically creates that map, but media is usually uploaded by the users so it does'nt know how to get to them.

# the plus sign is for concatanating the two arrays.
