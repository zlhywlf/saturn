from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from saturn.web.api import views

router = routers.DefaultRouter()
router.register(r"client", views.ClientViewSet)

urlpatterns = [
    path("auth", TokenObtainPairView.as_view(), name="auth"),
    path("", include(router.urls)),
]
