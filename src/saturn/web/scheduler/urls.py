from django.urls import path

from saturn.web.scheduler import views

urlpatterns = [
    path("", views.index, name="index"),
]
