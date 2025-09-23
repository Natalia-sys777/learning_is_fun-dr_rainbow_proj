from lessons.models import Lesson, Exercise

data = [
    {
        "slug": "energy-around-us",
        "title": "⚡ Енергія навколо нас",
        "summary": "Що таке енергія? Як вона працює?",
        "level": "середній",
        "duration": 20,
        "age_range": "6–9",
        "materials": "м'яч, ліхтарик, термос, батарейка",
        "steps": "Розглянь предмети; Поясни, як вони дають енергію; Визнач вид енергії",
        "assistant_image": "images/assistant_boy.png",
        "theory": "Енергія — це те, що змушує все рухатись, світитись, нагріватись...",
        "parent_notes": {
            "intro": "Поясніть дитині, що енергія допомагає всьому працювати.",
            "tips": ["Слідкуйте, які предмети потребують енергії."],
            "questions": ["Чи є енергія в тобі?", "Як ти використовуєш енергію щодня?"]
        },
        "exercises": [
            {
                "title": "Енергія в дії",
                "instructions": "Покоти м'яч, увімкни ліхтарик — які види енергії ти бачиш?",
                "difficulty": "easy",
                "duration": 5
            }
        ]
    },
    {
        "slug": "materials-and-properties",
        "title": "🧱 Властивості матеріалів",
        "summary": "Які бувають матеріали і як їх розпізнати?",
        "level": "легкий",
        "duration": 25,
        "age_range": "5–8",
        "materials": "дерево, пластик, скло, метал, вода",
        "steps": "Досліди матеріали; Торкнись, порівняй; Визнач їх властивості",
        "assistant_image": "images/assistant_girl.png",
        "theory": "Матеріали мають різні властивості: твердість, прозорість, гнучкість тощо.",
        "parent_notes": {
            "intro": "Допоможіть дитині класифікувати матеріали вдома.",
            "tips": ["Порівняйте ложку з дерева та металу."],
            "questions": ["Що твердіше — скло чи пластик?"]
        },
        "exercises": [
            {
                "title": "Розпізнай матеріал",
                "instructions": "Покажи предмет і спробуй назвати, з чого він зроблений.",
                "difficulty": "medium",
                "duration": 6
            }
        ]
    },
    {
        "slug": "plants-and-growth",
        "title": "🌱 Як ростуть рослини",
        "summary": "Що потрібно рослинам, щоб рости?",
        "level": "середній",
        "duration": 30,
        "age_range": "6–9",
        "materials": "насіння, горщик, вода, лампа, ґрунт",
        "steps": "Посади насіння; Полий; Постав на світло",
        "assistant_image": "images/assistant_plant.png",
        "theory": "Рослинам потрібні світло, вода, повітря та ґрунт для росту.",
        "parent_notes": {
            "intro": "Посадіть щось разом із дитиною.",
            "tips": ["Спостерігайте разом за ростом рослини."],
            "questions": ["Що станеться, якщо не поливати рослину?"]
        },
        "exercises": [
            {
                "title": "Експеримент з водою",
                "instructions": "Полий одну рослину, а іншу ні. Що відбувається за кілька днів?",
                "difficulty": "hard",
                "duration": 10
            }
        ]
    }
]


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

    for index, ex in enumerate(item.get("exercises", [])):
        Exercise.objects.get_or_create(
            lesson=lesson,
            title=ex["title"],
            defaults={
                "instructions": ex.get("instructions", ""),
                "order": ex.get("order", index),
                "difficulty": ex.get("difficulty", ""),
                "duration": ex.get("duration", 0),
            }
        )

    print(f"Урок '{lesson.title}' успішно {'створено' if created else 'знайдено'} з {len(item.get('exercises', []))} вправами.")
