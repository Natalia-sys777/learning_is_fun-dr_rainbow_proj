from django.core.management.base import BaseCommand
from lessons.models import Lesson, Exercise
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Завантажує стартові уроки з вправами у базу даних"

    def handle(self, *args, **options):
        lessons_data = [
            {
                "title": "🔍 Що таке фізика?",
                "emoji": "🔍",
                "summary": "Дізнаємось, що таке фізика і чому вона всюди навколо нас!",
                "level": "дуже легко",
                "duration": 10,
                "age_range": "6–9",
                "materials": "книга, м’ячик, ложка, магніт (не обов’язково)",
                "steps": "Подивись на різні предмети навколо; Подумай, як вони рухаються або працюють; Обговори разом, як це пов’язано з фізикою",
                "assistant_image": "images/assistant_boy.png",
                "theory": "🔍 Фізика — це наука, яка допомагає дізнатися, чому предмети падають, як щось рухається, звідки береться світло і як чути звук.",
                "safety_note": "",
                "exercises": [
                    {
                        "title": "Знайди фізику навколо",
                        "instructions": "Подивись навколо — що з того, що ти бачиш, можна пояснити фізикою?"
                    },
                    {
                        "title": "Спробуй пояснити",
                        "instructions": "Візьми будь-який предмет і спробуй сказати, чому він працює саме так."
                    }
                ]
            },
            # 🔁 Можеш додати тут більше уроків у тому ж форматі
        ]

        for data in lessons_data:
            slug = slugify(data["title"])
            lesson = Lesson.objects.filter(slug=slug).first()

            if not lesson:
                lesson = Lesson(
                    title=data["title"],
                    emoji=data["emoji"],
                    summary=data["summary"],
                    level=data["level"],
                    duration=data["duration"],
                    age_range=data["age_range"],
                    materials=data["materials"],
                    steps=data["steps"],
                    assistant_image=data["assistant_image"],
                    theory=data["theory"],
                    safety_note=data["safety_note"],
                    slug=slug
                )
                lesson.save()

            for ex_data in data["exercises"]:
                ex_slug = slugify(ex_data["title"])
                Exercise.objects.get_or_create(
                    slug=ex_slug,
                    lesson=lesson,
                    defaults={
                        "title": ex_data["title"],
                        "instructions": ex_data["instructions"],
                    }
                )

        self.stdout.write(self.style.SUCCESS("🎉 Уроки та вправи успішно завантажено!"))
