from django.db import models

class GeometryLesson(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    emoji = models.CharField(max_length=10, blank=True)
    summary = models.TextField()
    level = models.CharField(max_length=30)
    shape_focus = models.CharField(max_length=50, blank=True)
    materials = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    image = models.ImageField(upload_to='geometry/', blank=True)
    theory = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GeometryExercise(models.Model):
    lesson = models.ForeignKey(GeometryLesson, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=100)
    instructions = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} → {self.lesson.title}"




