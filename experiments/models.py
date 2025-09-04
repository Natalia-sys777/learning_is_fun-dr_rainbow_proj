from django.db import models
from django.utils.text import slugify

class Experiment(models.Model):
    EASY_CHOICES = [
        ("very-easy", "дуже легко"),
        ("easy", "легко"),
        ("medium", "середньо"),
    ]
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    emoji = models.CharField(max_length=4, default="🌈")
    level = models.CharField(max_length=20, choices=EASY_CHOICES, default="very-easy")
    summary = models.TextField(blank=True)
    materials = models.TextField(blank=True, help_text="через кому")
    steps = models.TextField(blank=True, help_text="кроки через крапку з комою")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

