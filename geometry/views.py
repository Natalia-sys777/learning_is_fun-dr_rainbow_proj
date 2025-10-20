from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import GeometryLesson, GeometryExercise
from django.db.models import Count, Q
import random

class GeometryLessonListView(ListView):
    """
    Список геометричних уроків з фільтром і пошуком.
    """
    model = GeometryLesson
    template_name = 'geometry/geometry_lesson_list.html'
    context_object_name = 'lessons'
    paginate_by = 12
    ordering = ['-created_at']

    def get_queryset(self):
        qs = (
            GeometryLesson.objects
            .all()
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


class GeometryLessonDetailView(DetailView):
    """
    Детальна сторінка уроку з геометрії з вправами.
    """
    model = GeometryLesson
    template_name = 'geometry/geometry_lesson_detail.html'
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'

    def get_queryset(self):
        return GeometryLesson.objects.prefetch_related('exercises')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lesson = ctx['lesson']
        ctx['exercises'] = lesson.exercises.all().order_by('id')

        # Опрацювання списків
        ctx['materials_list'] = [s.strip() for s in lesson.materials.split(',') if s.strip()]
        ctx['steps_list'] = [s.strip() for s in lesson.steps.split(';') if s.strip()]

        # Рекомендовані
        ctx['related_lessons'] = GeometryLesson.objects.exclude(pk=lesson.pk)[:6]

        return ctx
