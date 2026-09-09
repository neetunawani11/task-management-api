from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, TaskViewSet, RegisterView


router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
]

urlpatterns += router.urls