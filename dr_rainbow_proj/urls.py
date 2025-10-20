from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path("lessons/", include("lessons.urls")),
    path(
        "experiments/",
        include(("experiments.urls", "experiments"), namespace="experiments")),
    path("tasks/", include("tasks.urls")),
    path('geometry/', include('geometry.urls')),

]

