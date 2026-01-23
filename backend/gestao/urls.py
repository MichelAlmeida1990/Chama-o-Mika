"""
URL configuration for gestao project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from .views import login_view, logout_view, user_view, csrf_token_view
from .deploy_views import create_deploy_users_view, check_deploy_status_view

def api_root(request):
    """API root endpoint"""
    return JsonResponse({
        'message': 'SmartManager API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'estoque': '/api/estoque/',
            'financeiro': '/api/financeiro/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api_root'),
    path('api/', include('estoque.urls')),
    path('api/', include('financeiro.urls')),
    path('api/auth/csrf-token/', csrf_token_view, name='csrf-token'),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/user/', user_view, name='user'),
    path('api/auth/', include('rest_framework.urls')),
    # Endpoints especiais para deploy
    path('deploy/create-users/', create_deploy_users_view, name='deploy-create-users'),
    path('deploy/status/', check_deploy_status_view, name='deploy-status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

