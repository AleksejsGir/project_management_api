from django.urls import path
from rest_framework.routers import DefaultRouter

# Пока создаем пустой urlpatterns, позже добавим ViewSets
urlpatterns = [
    # Временно пустой, добавим маршруты когда создадим views
]

# Роутер для ViewSets (добавим позже)
router = DefaultRouter()

# Добавляем роутер к urlpatterns
urlpatterns += router.urls