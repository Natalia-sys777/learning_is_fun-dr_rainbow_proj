from django.urls import path
from . import views

app_name = "experiments"

urlpatterns = [
    path("", views.experiments_list, name="experiments"),
    path("manage/", views.experiments_manage, name="experiments_manage"),
    path("quick-add/", views.experiments_quick_add, name="experiments_quick_add"),
    path("random/", views.experiment_random, name="experiments_random"),
    path("<slug:slug>/", views.ExperimentDetailView.as_view(), name="experiments_detail_static"),
    path("sound-lesson/", views.sound_lesson, name="sound_lesson"),


]


