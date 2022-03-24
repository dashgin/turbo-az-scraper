from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from cars import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='cars/index.html')),
    path('api/cars/', views.get_numbers_view),
    path('api/cars/all/', views.get_numbers),
]
