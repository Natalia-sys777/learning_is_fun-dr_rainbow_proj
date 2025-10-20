from django.urls import path
from .views import GeometryLessonListView, GeometryLessonDetailView

app_name = 'geometry'

urlpatterns = [
    path('', GeometryLessonListView.as_view(), name='lesson_list'),
    path('<slug:lesson_slug>/', GeometryLessonDetailView.as_view(), name='lesson_detail'),
]
