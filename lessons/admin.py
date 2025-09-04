from django.contrib import admin
from django.db.models import Count
from .models import Lesson, Exercise


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 0

    show_change_link = True


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at", "exercises_count")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ExerciseInline]
    ordering = ("created_at", "id")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_ex_cnt=Count("exercises", distinct=True))

    def exercises_count(self, obj):
        return getattr(obj, "_ex_cnt", obj.exercises.count())
    exercises_count.short_description = "Вправ"


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "difficulty", "duration", "order")
    list_filter = ("lesson", "difficulty")
    search_fields = ("title", "instructions", "hints")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("lesson", "order", "id")
