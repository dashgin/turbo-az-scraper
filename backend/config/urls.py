from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from cars import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("404/", TemplateView.as_view(template_name="cars/404.html")),
    path("", views.index),
    path("api/cars/", views.get_numbers_view),
    path("api/cars/all/", views.get_numbers),
]
