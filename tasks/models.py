from django.db import models
from django.urls import reverse

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва завдання")
    slug = models.SlugField(unique=True, verbose_name="URL-псевдонім")
    instructions = models.TextField(verbose_name="Інструкція")
    level = models.CharField(max_length=50, blank=True, verbose_name="Рівень")
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name="Тривалість (хв)")
    image = models.ImageField(upload_to="tasks/", blank=True, null=True, verbose_name="Зображення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"
        ordering = ["created_at", "id"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"task_slug": self.slug})

