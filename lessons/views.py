from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from .models import Lesson, Exercise
import random


class LessonListView(ListView):
    """
    Список уроків з пошуком, фільтром за складністю і пагінацією.
    """
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    context_object_name = 'lessons'
    paginate_by = 12
    ordering = ['-created_at']

    def get_queryset(self):
        qs = (
            Lesson.objects
            .filter(is_public=True)  # ✅ показуємо тільки доступні уроки
            .annotate(exercises_count=Count('exercises', distinct=True))
        )

        q = self.request.GET.get('q', '').strip()
        level = self.request.GET.get('level', '').strip()

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(summary__icontains=q) |
                Q(materials__icontains=q) |
                Q(steps__icontains=q)
            )

        if level:
            qs = qs.filter(level=level)

        return qs.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['level'] = self.request.GET.get('level', '')
        return ctx


class LessonDetailView(DetailView):
    """
    Детальна сторінка уроку з вправами, матеріалами, кроками та асистентом.
    """
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'

    def get_queryset(self):
        return Lesson.objects.prefetch_related('exercises')

    def _split_field(self, value, sep):
        if not value:
            return []
        if isinstance(value, (list, tuple)):
            return [s for s in value if str(s).strip()]
        return [s.strip() for s in str(value).split(sep) if s.strip()]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = context['lesson']
        parent_notes = getattr(lesson, 'parent_notes', {}) or {}
        context['parent_notes_intro'] = parent_notes.get('intro')
        context['parent_notes_tips'] = parent_notes.get('tips', [])
        context['parent_notes_questions'] = parent_notes.get('questions', [])

        # Вправи
        exercises_qs = lesson.exercises.all()
        if 'order' in [f.name for f in Exercise._meta.fields]:
            exercises_qs = exercises_qs.order_by('order', 'id')
        else:
            exercises_qs = exercises_qs.order_by('created_at', 'id')
        context['exercises'] = exercises_qs

        # Матеріали та кроки
        context['materials_list'] = self._split_field(lesson.materials, ',')
        context['steps_list'] = self._split_field(lesson.steps, ';')
        context['materials_list'] = [s.strip() for s in lesson.materials.split(',') if s.strip()]


        # Схожі уроки
        context['related_lessons'] = Lesson.objects.exclude(pk=lesson.pk).filter(level=lesson.level, is_public=True)[:6]

        # Випадкові (сюрприз)
        context['random_lessons'] = Lesson.objects.exclude(pk=lesson.pk).filter(is_public=True).order_by('?')[:5]

        # Асистент (автоматично, якщо не задано)
        if not lesson.assistant_image:
            title = lesson.title.lower()
            if 'звук' in title or 'вібрац' in title:
                context['assistant_image'] = 'images/assistant_boy.png'
            elif 'світло' in title or 'тін' in title:
                context['assistant_image'] = 'images/assistant_girl.png'
            elif 'швидкість' in title or 'рух' in title:
                context['assistant_image'] = 'images/assistant_rainbow.png'
            else:
                context['assistant_image'] = random.choice([
                    'images/assistant_boy.png',
                    'images/assistant_girl.png',
                    'images/assistant_rainbow.png'
                ])
        else:
            context['assistant_image'] = lesson.assistant_image

        return context


class ExerciseListView(ListView):
    """
    Всі вправи (або вправи до конкретного уроку).
    """
    model = Exercise
    template_name = "lessons/exercise_list.html"
    context_object_name = "exercises"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset().select_related("lesson").order_by("lesson__title", "id")
        lesson_slug = self.kwargs.get("lesson_slug")
        if lesson_slug:
            self.lesson = get_object_or_404(Lesson, slug=lesson_slug)
            qs = qs.filter(lesson=self.lesson)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if hasattr(self, "lesson"):
            ctx["lesson"] = self.lesson
        return ctx


class ExerciseDetailView(DetailView):
    """
    Детальна сторінка вправи.
    """
    model = Exercise
    template_name = "lessons/exercise_detail.html"
    context_object_name = "exercise"
    slug_url_kwarg = "exercise_slug"
