from lessons.models import Lesson, Exercise
import uuid

data = [{
        "slug": "energy-around-us",
        "title": "⚡ Енергія навколо нас",
        "summary": "Що таке енергія? Як вона працює?",
        "level": "середній",
        "duration": 20,
        "age_range": "6–9",
        "materials": "м'яч, ліхтарик, термос, батарейка",
        "steps": "Розглянь предмети; Поясни, як вони дають енергію; Визнач вид енергії",
        "assistant_image": "images/assistant_boy.png",
        "theory": "Енергія — це те, що змушує все рухатись, світитись, нагріватись. Є різні види енергії: рух, тепло, світло, звук.",
        "parent_notes": {
            "intro": "Поясніть дитині, що енергія — це те, що допомагає речам рухатись або світитись...",
            "tips": [
                "Спостерігайте разом, які предмети світяться, гріють або рухаються.",
                "Пограйте у гру: знайди 5 речей, які споживають енергію."
            ],
            "questions": [
                "А ти можеш придумати ще приклади енергії?",
                "Яка енергія потрібна, щоб приготувати чай?"
            ]
        },
        "exercises": [
            {
                "title": "Енергія в дії",
                "instructions": "Покоти м'яч, увімкни ліхтарик — які види енергії ти бачиш?"
            },
            {
                "title": "Хто дає енергію?",
                "instructions": "Знайди 3 предмети в кімнаті, які працюють завдяки енергії."
            }
        ]
    },
]# сюди встав список словників з уроками

for item in data:
    lesson, created = Lesson.objects.get_or_create(
        slug=item["slug"],
        defaults={
            "title": item["title"],
            "summary": item["summary"],
            "level": item["level"],
            "duration": item["duration"],
            "age_range": item["age_range"],
            "materials": item["materials"],
            "steps": item["steps"],
            "assistant_image": item["assistant_image"],
            "theory": item["theory"],
            "parent_notes": item["parent_notes"]
        }
    )
    for ex in item.get("exercises", []):
        Exercise.objects.get_or_create(
            lesson=lesson,
            title=ex["title"],
            defaults={"instructions": ex["instructions"]}
        )

