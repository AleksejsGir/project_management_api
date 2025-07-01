from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register ViewSets
router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'vacancies', views.VacancyViewSet, basename='vacancy')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# This will create the following URL patterns:
#
# Project URLs:
# GET    /api/projects/              - List all projects
# POST   /api/projects/              - Create new project
# GET    /api/projects/{id}/         - Get specific project
# PUT    /api/projects/{id}/         - Update project (full)
# PATCH  /api/projects/{id}/         - Update project (partial)
# DELETE /api/projects/{id}/         - Delete project
# GET    /api/projects/{id}/vacancies/ - Get project vacancies
# POST   /api/projects/{id}/vacancies/ - Create vacancy for project
# GET    /api/projects/{id}/stats/   - Get project statistics
#
# Vacancy URLs:
# GET    /api/vacancies/             - List all vacancies
# GET    /api/vacancies/{id}/        - Get specific vacancy
# PUT    /api/vacancies/{id}/        - Update vacancy (full)
# PATCH  /api/vacancies/{id}/        - Update vacancy (partial)
# DELETE /api/vacancies/{id}/        - Delete vacancy