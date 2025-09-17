from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.urls import reverse
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

    lessons = [
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
            "theory": "Енергія — це те, що змушує все рухатись, світитись, нагріватись. Є різні види енергії: рух, тепло, світло, звук.",
            "exercises": [
                {
                    "title": "Енергія в дії",
                    "instructions": "Покоти м'яч, увімкни ліхтарик — які види енергії ти бачиш?"
                },
                {
                    "title": "Хто дає енергію?",
                    "instructions": "Знайди 3 предмети в кімнаті, які працюють завдяки енергії."
                }
            ],
            "parent_notes": {
                "intro": "Поясніть дитині, що енергія — це те, що допомагає речам рухатись або світитись. Покажіть на прикладах: м’яч рухається — це рухома енергія, ліхтарик світиться — це світлова енергія.",
                "tips": [
                    "Спостерігайте разом, які предмети світяться, гріють або рухаються.",
                    "Пограйте у гру: знайди 5 речей, які споживають енергію."
                ],
                "questions": [
                    "А ти можеш придумати ще приклади енергії?",
                    "Яка енергія потрібна, щоб приготувати чай?"
                ]
            }
        },
        {
            "slug": "water-and-steam",
            "title": "💧 Вода і пар",
            "summary": "Як вода перетворюється на пар?",
            "level": "середній",
            "duration": 20,
            "age_range": "6–9",
            "materials": "банка з водою, чайник, ложка, лід",
            "steps": "Нагрій воду; Спостерігай пар; Подивись, як тане лід",
            "assistant_image": "images/assistant_girl.png",
            "theory": "Коли вода нагрівається — вона перетворюється на пар. А коли охолоджується — стає льодом.",
            "exercises": [
                {
                    "title": "Дим з чайника",
                    "instructions": "Спостерігай, як з чайника йде пар. Це — вода в газоподібному стані."
                },
                {
                    "title": "Танення льоду",
                    "instructions": "Поклади лід на ложку. Як він змінюється з часом?"
                }
            ],
            "parent_notes": {
                "intro": "Цей урок добре ілюструє зміну станів речовини. Поясніть дитині, що вода може бути рідиною, парою або льодом, але завжди залишається водою.",
                "tips": [
                    "Проведіть дослід: лід → вода → пар.",
                    "Поясніть, що 'дим' над чайником — це мікрокраплі води."
                ],
                "questions": [
                    "Чому чайник 'димить'?",
                    "Чи справді пар видно?"
                ]
            }
        },
        {
            "slug": "electricity-and-safety",
            "title": "🔌 Електрика і безпека",
            "summary": "Що таке струм? Як бути обережним?",
            "level": "середній",
            "duration": 25,
            "age_range": "6–9",
            "materials": "батарейка, лампочка, дроти, схеми",
            "steps": "Збери ланцюг; Увімкни лампочку; Обговори правила безпеки",
            "assistant_image": "images/assistant_boy.png",
            "theory": "Електрика — це енергія, яка рухається по дротах. Вона може бути небезпечною, якщо нею неправильно користуватись.",
            "exercises": [
                {
                    "title": "Лампочка світиться",
                    "instructions": "Збери простий ланцюг із батарейки, лампочки і дротів."
                },
                {
                    "title": "Безпечна електрика",
                    "instructions": "Назви 3 правила, як безпечно поводитись із розетками й приладами."
                }
            ],
            "parent_notes": {
                "intro": "Електрика корисна, але небезпечна. Дитина має розуміти, що з нею потрібно бути обережною.",
                "tips": [
                    "Покажіть побутові прилади й поясніть, як вони працюють.",
                    "Зберіть разом просте коло з лампочкою й батарейкою."
                ],
                "questions": [
                    "Чому не можна вставляти нічого в розетку?",
                    "Які прилади вдома працюють на електриці?"
                ]
            }
        },
        {
            "slug": "levers-and-balance",
            "title": "⚖️ Важелі і рівновага",
            "summary": "Як працює гойдалка? Що таке баланс?",
            "level": "середній",
            "duration": 20,
            "age_range": "6–9",
            "materials": "дошка, олівець, фішки або монети",
            "steps": "Зроби гойдалку; Розклади вантажі; Шукай рівновагу",
            "assistant_image": "images/assistant_girl.png",
            "theory": "Важіль — це пристрій, що дозволяє легко піднімати або балансувати щось. Якщо обидва боки важать однаково — є рівновага.",
            "exercises": [
                {
                    "title": "Гойдалка в рівновазі",
                    "instructions": "Розмісти фішки на дошці. Коли вона буде в балансі?"
                },
                {
                    "title": "Сила і відстань",
                    "instructions": "Що буде, якщо фішку покласти ближче до середини або далі?"
                }
            ],
            "parent_notes": {
                "intro": "Важелі — приклад того, як фізика допомагає в повсякденному житті. Гойдалки, ножиці, дверна ручка — все це важелі.",
                "tips": [
                    "Пограйте з дитиною в рівновагу: фішки, олівець, дошка.",
                    "Поясніть, що важіль дає перевагу у зусиллі."
                ],
                "questions": [
                    "Де ти бачив(ла) важелі у повсякденному житті?",
                    "Що допомагає гойдалці залишатись у балансі?"
                ]
            }
        }
    ]

    def get_queryset(self):
        qs = (
            Lesson.objects
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
        parent_notes = lesson.get('parent_notes', {}) if isinstance(lesson, dict) else getattr(lesson, 'parent_notes',
                                                                                               {}) or {}
        context['parent_notes_intro'] = parent_notes.get('intro')
        context['parent_notes_tips'] = parent_notes.get('tips', [])
        context['parent_notes_questions'] = parent_notes.get('questions', [])

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

        # Схожі уроки
        context['related_lessons'] = Lesson.objects.exclude(pk=lesson.pk).filter(level=lesson.level)[:6]

        # Випадкові (сюрприз)
        context['random_lessons'] = Lesson.objects.exclude(pk=lesson.pk).order_by('?')[:5]

        # Асистент (автоматично, якщо не задано)
        if not lesson.assistant_image:
            title = lesson.title.lower()
            if 'звук' in title or 'вібрац' in title:
                context['assistant_image'] = 'images/assistant_boy.png'
            elif 'світло' in title or 'тін' in title:
                context['assistant_image'] = 'images/assistant_girl.png'
            elif 'швидкість' in title or 'тін' in title:
                context['assistant_image'] = 'images/assistant_rainbow .png'
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