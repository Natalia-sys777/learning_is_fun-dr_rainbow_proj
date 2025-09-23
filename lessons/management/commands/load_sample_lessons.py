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
                "theory": """
🔍 Фізика — це наука, яка допомагає дізнатися, чому предмети падають, як щось рухається, звідки береться світло і як чути звук.
Це як чарівні окуляри: надягаєш — і бачиш, як працює світ навколо тебе!
""",
                "safety_note": "",
                "exercises": [
                    {
                        "title": "Знайди фізику навколо",
                        "instructions": "Подивись навколо — що з того, що ти бачиш, можна пояснити фізикою? Наприклад, чому м’яч котиться?",
                        "difficulty": "easy",
                        "duration": 5
                    },
                    {
                        "title": "Спробуй пояснити",
                        "instructions": "Візьми будь-який предмет і спробуй сказати, чому він працює саме так. Наприклад, чому ложка падає, коли її відпустити?",
                        "difficulty": "medium",
                        "duration": 7
                    }
                ]
            },
            {
                "title": "⚖️ Що таке маса?",
                "emoji": "⚖️",
                "summary": "Вчимося розрізняти масу предметів — що важке, а що легке?",
                "level": "легко",
                "duration": 15,
                "age_range": "6–9",
                "materials": "ваги, яблуко, камінчик, подушка",
                "steps": "Порівняй два предмети; Поклади їх на ваги; Подивись, який важчий",
                "assistant_image": "images/assistant_girl.png",
                "theory": """
⚖️ Маса — це те, скільки важить предмет. Деякі речі легкі (як подушка), а деякі — важкі (як камінь).
Ми можемо виміряти масу за допомогою ваг.
""",
                "safety_note": "Будьте обережні з важкими предметами — не кидайте їх і не кладіть на край стола.",
                "exercises": [
                    {
                        "title": "Що важче?",
                        "instructions": "Візьми два предмети та порівняй, який важчий. Наприклад, яблуко і книжка.",
                        "difficulty": "easy",
                        "duration": 5
                    },
                    {
                        "title": "Вгадай масу",
                        "instructions": "Запропонуй дітям вгадати, скільки важить предмет, а потім перевірити на вагах.",
                        "difficulty": "medium",
                        "duration": 7
                    }
                ]
            },
            {
                "title": "🧪 Що таке об'єм?",
                "emoji": "🧪",
                "summary": "Навчимося розуміти, скільки місця займає вода чи інші речовини.",
                "level": "легко",
                "duration": 15,
                "age_range": "6–9",
                "materials": "склянка, пляшка, мірний стакан, вода",
                "steps": "Налий воду в різні ємності; Подивись, де її більше; Порівняй об’єм",
                "assistant_image": "images/assistant_girl.png",
                "theory": """
🧪 Об'єм — це скільки місця щось займає. Наприклад, вода в пляшці займає більше місця, ніж у склянці.
Об'єм можна вимірювати в мілілітрах або літрах.
""",
                "safety_note": "Працюйте з водою обережно, щоб нічого не розлити на електроприлади.",
                "exercises": [
                    {
                        "title": "Порівняй об’єм",
                        "instructions": "Налий воду в дві різні посудини. Подивись, де більше. Обговори чому.",
                        "difficulty": "easy",
                        "duration": 5
                    },
                    {
                        "title": "Міряємо об’єм",
                        "instructions": "Використай мірний стакан, щоб виміряти, скільки мл влізло у склянку чи чашку.",
                        "difficulty": "medium",
                        "duration": 7
                    }
                ]
            }
        ]

        for data in lessons_data:
            clean_slug = slugify(data["title"], allow_unicode=False)

            lesson, created = Lesson.objects.get_or_create(
                slug=clean_slug,
                defaults={
                    "title": data["title"],
                    "emoji": data["emoji"],
                    "summary": data["summary"],
                    "level": data["level"],
                    "age_range": data["age_range"],
                    "duration": data["duration"],
                    "materials": data["materials"],
                    "steps": data["steps"],
                    "assistant_image": data["assistant_image"],
                    "theory": data["theory"],
                    "safety_note": data["safety_note"],
                }
            )

            for i, ex_data in enumerate(data["exercises"]):
                Exercise.objects.get_or_create(
                    slug=slugify(ex_data["title"], allow_unicode=False),
                    lesson=lesson,
                    defaults={
                        "title": ex_data["title"],
                        "instructions": ex_data["instructions"],
                        "difficulty": ex_data.get("difficulty", "medium"),
                        "duration": ex_data.get("duration", 5),
                        "order": i + 1,
                    }
                )

        self.stdout.write(self.style.SUCCESS("🎉 Уроки та вправи успішно завантажено!"))
