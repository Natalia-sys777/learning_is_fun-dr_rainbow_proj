from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "level", "duration", "created_at", "preview_image")
    search_fields = ("title", "instructions")
    list_filter = ("lesson", "level", "created_at")
    prepopulated_fields = {"slug": ("title",)}

    def preview_image(self, obj):
        if obj.image:
            return f"✅"
        return "—"
    preview_image.short_description = "Зображення"

