from django.core.management.base import BaseCommand
from lessons.models import Lesson, Exercise
from django.utils.text import slugify
import random


LESSONS = [
    {
        "title": "🔦 У пошуках тіні",
        "emoji": "🔦",
        "summary": "Вивчаємо світло і тінь",
        "level": "легко",
        "duration": 20,
        "age_range": "6–8",
        "materials": "ліхтарик, аркуш паперу, ручка",
        "steps": "Увімкни ліхтарик; Направ на руку; Спостерігай за тінню",
        "assistant_image": "images/assistant_girl.png",
        "theory": """
🔦 Що таке світло?

Світло дозволяє нам бачити. Воно поширюється прямо і створює тіні, коли натрапляє на предмет.

🌑 Темрява — це відсутність світла.

🎭 Тінь — це область, куди не потрапляє світло через перешкоду.

🌈 Світло може:
- рухатись прямо
- створювати тіні
- відбиватись
- бути кольоровим
""",
        "exercises": [
            {
                "title": "Знайди свою тінь",
                "instructions": "Покажи ліхтариком на предмет і подивись, як утворюється тінь.",
            },
            {
                "title": "Гра з тінями",
                "instructions": "Створи тінь тварини руками.",
            },
        ]
    },
    {
        "title": "🎧 Подорож звуком",
        "emoji": "🎧",
        "summary": "Що таке звук і вібрація?",
        "level": "легко",
        "duration": 15,
        "age_range": "6–9",
        "materials": "гумка, лінійка, стіл",
        "steps": "Натягни гумку; Удар її і слухай звук; Поклади лінійку на стіл, натисни і відпусти",
        "assistant_image": "images/assistant_boy.png",
        "theory": """
🎧 Що таке звук?

Звук — це коливання (вібрації), які поширюються через повітря або інші матеріали. Наші вуха вловлюють ці вібрації — і ми чуємо звук.

🔊 Властивості звуку:
- Поширюється через повітря
- Має гучність і висоту
- Виникає через вібрації
""",
        "exercises": [
            {
                "title": "Вгадай джерело звуку",
                "instructions": "Послухай звук із закритими очима і здогадайся, звідки він лунає.",
            },
            {
                "title": "Слухай і вгадуй",
                "instructions": "Прослухай звук і спробуй назвати його джерело.",
            },
        ]
    },
    {
        "title": "🧲 Магнітні дива",
        "emoji": "🧲",
        "summary": "Досліджуємо, як працюють магніти",
        "level": "середньо",
        "duration": 20,
        "age_range": "7–10",
        "materials": "магніт, скріпки, ложка, аркуш паперу",
        "steps": "Проведи магнітом над предметами; Подивись, що притягується; Спробуй через папір",
        "assistant_image": "images/assistant_boy.png",
        "theory": """
🧲 Що таке магніт?

Магніти притягують деякі предмети, особливо ті, що містять залізо. Вони мають два полюси — північний і південний.

🔍 Цікаві факти:
- Деякі предмети не реагують на магніт.
- Магніти можуть притягувати через тонкі речі (наприклад, папір).
""",
        "exercises": [
            {
                "title": "Магнітний детектив",
                "instructions": "Знайди 5 предметів, які притягує магніт.",
            },
            {
                "title": "Магніт через папір",
                "instructions": "Спробуй притягнути скріпку через аркуш паперу.",
            },
        ]
    },
    {
        "title": "🌍 Сила тяжіння",
        "emoji": "🌍",
        "summary": "Дізнаємось, чому предмети падають вниз",
        "level": "легко",
        "duration": 15,
        "age_range": "6–8",
        "materials": "м'яч, перо, аркуш паперу",
        "steps": "Підкинь м'яч; Підкинь перо; Порівняй, як вони падають",
        "assistant_image": "images/assistant_girl.png",
        "theory": """
🌍 Що таке сила тяжіння?

Це сила, яка тягне все до Землі. Саме через неї предмети падають вниз.

🧪 Цікаво знати:
- Сила тяжіння діє на всі предмети.
- Деякі предмети падають повільніше через опір повітря.
""",
        "exercises": [
            {
                "title": "Що швидше падає?",
                "instructions": "Порівняй падіння м'яча і пера.",
            },
            {
                "title": "Стрибай високо!",
                "instructions": "Спробуй стрибнути і відчути, як земля тебе притягує назад.",
            },
        ]
    },
    {
        "title": "🌈 Барви веселки",
        "emoji": "🌈",
        "summary": "Як утворюється веселка і які в неї кольори",
        "level": "легко",
        "duration": 15,
        "age_range": "6–9",
        "materials": "склянка води, ліхтарик, дзеркальце",
        "steps": "Налий воду в склянку; Поклади дзеркальце; Посвіти ліхтариком і спостерігай кольори",
        "assistant_image": "images/assistant_girl.png",
        "theory": """
🌈 Як з'являється веселка?

Веселка виникає, коли світло проходить через краплі води і розкладається на кольори.

🎨 Кольори веселки:
- червоний
- оранжевий
- жовтий
- зелений
- блакитний
- синій
- фіолетовий
""",
        "exercises": [
            {
                "title": "Створи веселку",
                "instructions": "Зроби веселку вдома з водою і світлом.",
            },
            {
                "title": "Запам'ятай кольори",
                "instructions": "Перерахуйте разом усі 7 кольорів веселки.",
            },
        ]
    }
]



from django.core.management.base import BaseCommand
from lessons.models import Lesson, Exercise
from django.utils.text import slugify
import random

# 🧪 Додай сюди свій список LESSONS, якщо потрібно

def generate_unique_slug(model, base, max_length=50):
    slug = slugify(base)[:max_length]
    original_slug = slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        suffix = f"-{counter}"
        slug = f"{original_slug[:max_length - len(suffix)]}{suffix}"
        counter += 1
    return slug


class Command(BaseCommand):
    help = "Заповнює базу кількома уроками та вправами"

    def add_arguments(self, parser):
        parser.add_argument('--cleanup', action='store_true', help='Видалити уроки з порожніми або невалідними slug')

    def handle(self, *args, **options):
        if options['cleanup']:
            self.cleanup_invalid_lessons()

        created_count = 0
        for data in LESSONS:
            slug = slugify(data["title"], allow_unicode=True).strip()
            if not slug:
                self.stdout.write(self.style.WARNING(f"⚠️ Пропущено урок без slug: {data['title']}"))
                continue

            lesson, created = Lesson.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": data["title"],
                    "emoji": data["emoji"],
                    "summary": data["summary"],
                    "level": data["level"],
                    "duration": data["duration"],
                    "age_range": data["age_range"],
                    "materials": data["materials"],
                    "steps": data["steps"],
                    "assistant_image": data.get("assistant_image", random.choice([
                        "images/assistant_girl.png",
                        "images/assistant_boy.png"
                    ])),
                    "theory": data.get("theory", ""),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Створено урок: {lesson.title}"))
                created_count += 1
            else:
                self.stdout.write(f"↪️ Урок вже існує: {lesson.title}")

            for index, ex in enumerate(data["exercises"], start=1):
                Exercise.objects.get_or_create(
                    lesson=lesson,
                    title=ex["title"],
                    defaults={
                        "instructions": ex["instructions"],
                        "slug": generate_unique_slug(Exercise, ex["title"]),
                        "order": index,
                    }
                )
        self.stdout.write(self.style.SUCCESS(f"\n✨ Готово! Додано {created_count} нових уроків."))

    def cleanup_invalid_lessons(self):
        bad_lessons = Lesson.objects.filter(slug__isnull=True) | Lesson.objects.filter(slug="")
        count = bad_lessons.count()
        bad_lessons.delete()
        self.stdout.write(self.style.WARNING(f"🧹 Видалено {count} урок(ів) з порожнім slug."))
