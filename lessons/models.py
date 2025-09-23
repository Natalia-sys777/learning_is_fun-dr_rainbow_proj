from django.db import models
from django.utils.text import slugify

class Lesson(models.Model):
    title = models.CharField("Назва уроку", max_length=200)
    slug = models.SlugField(max_length=100, unique=True, blank=False)
    emoji = models.CharField("Емоджі", max_length=10, blank=True, null=True)
    summary = models.TextField("Короткий опис", blank=True, null=True)
    level = models.CharField("Рівень складності", max_length=50, blank=True, null=True)
    duration = models.PositiveIntegerField("Тривалість (хв)", blank=True, null=True)
    age_range = models.CharField("Вік", max_length=50, blank=True, null=True)
    materials = models.TextField("Матеріали", blank=True, null=True)
    steps = models.TextField("Кроки", blank=True, null=True)
    assistant_image = models.CharField("Зображення асистента", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    theory = models.TextField(blank=True, help_text="Текстовий опис для пояснення теорії")
    parent_notes = models.JSONField(null=True, blank=True)
    safety_note = models.TextField("Примітка з безпеки", blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✨ Ось ці поля додай:
    order = models.PositiveIntegerField(default=0, help_text="Порядок у уроці")
    difficulty = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('easy', 'Легко'),
            ('medium', 'Середньо'),
            ('hard', 'Важко'),
        ],
        help_text="Складність вправи"
    )
    duration = models.PositiveIntegerField(default=0, help_text="Тривалість (у хвилинах)")

    def __str__(self):
        return self.title
