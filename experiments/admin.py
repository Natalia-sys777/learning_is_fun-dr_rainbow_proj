from django.contrib import admin
from .models import Experiment

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "is_published", "updated_at")
    list_filter = ("is_published", "level")
    search_fields = ("title", "summary", "materials")
    prepopulated_fields = {"slug": ("title",)}
