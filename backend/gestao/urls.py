"""
URL configuration for gestao project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view, user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('estoque.urls')),
    path('api/', include('financeiro.urls')),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/user/', user_view, name='user'),
    path('api/auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

