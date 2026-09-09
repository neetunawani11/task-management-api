from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet

router = DefaultRouter()

router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)

urlpatterns = router.urls