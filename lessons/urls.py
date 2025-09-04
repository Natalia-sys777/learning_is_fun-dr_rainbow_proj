from django.urls import path, re_path
from .views import (
    LessonListView, LessonDetailView,
    ExerciseListView, ExerciseDetailView
)

urlpatterns = [
    path("", LessonListView.as_view(), name="lessons"),
    re_path(r"^lessons/(?P<lesson_slug>[\w\-]+)/$", LessonDetailView.as_view(), name="lesson_detail"),

    # ✅ список усіх вправ
    path("exercises/", ExerciseListView.as_view(), name="exercise_list"),

    # ✅ список вправ для конкретного уроку
    re_path(r'^lessons/(?P<lesson_slug>[-\wа-яА-ЯёЁіІїЇєЄґҐ]+)/exercises/$', ExerciseListView.as_view(), name='lesson_exercise_list'),
    path("exercises/<slug:exercise_slug>/", ExerciseDetailView.as_view(), name="exercise_detail"),
    # якщо у Exercise поки немає slug — використовуй pk:
    # path("exercises/<int:pk>/", ExerciseDetailView.as_view(), name="exercise_detail"),
    path("exercises/<slug:lesson_slug>/", ExerciseListView.as_view(), name="exercise_list")
]
