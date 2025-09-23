import json
from django.core.management.base import BaseCommand
from lessons.models import Lesson, Exercise
from django.utils.text import slugify
from pathlib import Path


class Command(BaseCommand):
    help = "Load sample lessons and exercises"

    def handle(self, *args, **kwargs):
        file_path = Path(__file__).resolve().parent.parent.parent / "data" / "lessons_data.json"

        with open(file_path, "r", encoding="utf-8") as f:
            lessons_data = json.load(f)

        for data in lessons_data:
            clean_slug = slugify(data["title"],
                                 allow_unicode=True) or f"lesson-{slugify(data['emoji'], allow_unicode=True)}"

            lesson, created = Lesson.objects.get_or_create(
                slug=clean_slug,
                defaults={
                    "title": data["title"],
                    "emoji": data["emoji"],
                    "summary": data["summary"],
                    "level": data["level"],
                    "age_range": data["age_range"],
                    "duration": data["duration"],
                    "safety_note": data.get("safety_note", ""),
                    "is_public": True
                },
            )

            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} lesson: {lesson.title}"))

            for i, ex_data in enumerate(data["exercises"]):
                # Гарантуємо slug для вправ
                raw_slug = slugify(ex_data["title"], allow_unicode=True)
                ex_slug = raw_slug or f"exercise-{i}-{clean_slug}"

                exercise, ex_created = Exercise.objects.get_or_create(
                    slug=ex_slug,
                    lesson=lesson,
                    defaults={
                        "title": ex_data["title"],
                        "instructions": ex_data["instructions"],
                        "order": i,
                        "difficulty": "easy",
                        "duration": 5,
                    },
                )

                self.stdout.write(
                    self.style.SUCCESS(f"  {'Created' if ex_created else 'Updated'} exercise: {exercise.title}"))

        self.stdout.write(self.style.SUCCESS("🎉 Уроки та вправи успішно завантажено!"))
