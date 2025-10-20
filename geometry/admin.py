from django.contrib import admin
from .models import GeometryLesson  # імпортуємо модель

@admin.register(GeometryLesson)
class GeometryLessonAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "duration", "created_at")
    search_fields = ("title", "summary", "materials")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("level", "age_range")

