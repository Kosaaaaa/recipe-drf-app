"""
App url routes
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health-check/', core_views.health_check, name='health-check'),
    path('api/factorial/<int:n>/', core_views.factorial_view, name='factorial'),
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
]

if settings.DEBUG:
    urlpatterns.extend([
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    ])
