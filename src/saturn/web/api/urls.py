from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("auth", TokenObtainPairView.as_view(), name="auth"),
]
