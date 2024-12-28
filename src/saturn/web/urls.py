from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

urlpatterns = [
    path("", lambda request: render(request, "index.html"), name="index"),
    path("admin/", admin.site.urls),
    path("api/", include("saturn.web.api.urls")),
]
