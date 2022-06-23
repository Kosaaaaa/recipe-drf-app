"""
URL mappings for the recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()

app_name = 'recipe'
router.register('recipes', views.RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
