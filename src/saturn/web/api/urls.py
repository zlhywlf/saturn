from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from saturn.web.api import views

router = routers.DefaultRouter()
router.register(r"client", views.ClientViewSet)
router.register(r"project", views.ProjectViewSet)
router.register(r"monitor", views.MonitorViewSet)
router.register(r"task", views.TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth", TokenObtainPairView.as_view(), name="auth"),
    path("status", views.status, name="status"),
    re_path(r"client_status/(\d+)", views.client_status, name="client_status"),
]
