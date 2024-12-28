from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from saturn.web.scheduler import views

urlpatterns = [
    path("api/index", views.index, name="index"),
    path("api/auth", TokenObtainPairView.as_view(), name="auth"),
]
