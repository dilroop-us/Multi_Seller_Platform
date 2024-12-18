from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # This includes the URLs from the core app
    path('', include('users.urls')),
]