from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from .views import register


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("buty_center.urls")),
    path("auth/", include("rest_framework.urls")),
    path("api/register/", register, name="register"),
]
