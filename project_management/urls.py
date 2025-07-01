from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import api_root

urlpatterns = [
    # Главная страница API
    path('', api_root, name='api-root'),

    # Админка
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('projects.urls')),
    path('auth/', include('authentication.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]