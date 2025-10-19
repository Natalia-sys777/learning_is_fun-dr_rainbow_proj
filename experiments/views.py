from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.http import Http404
import random

# 💾 Тимчасові "заготовки" (можеш замінити на модель пізніше)
EXPERIMENTS = {
    "home-rainbow": {
        "slug": "home-rainbow",
        "title": "Домашня веселка",
        "emoji": "🌈",
        "summary": "Склянка води + світло = кольори на стіні!",
        "materials": ["склянка з водою", "аркуш білого паперу", "ліхтарик або сонце"],
        "steps": [
            "Постав склянку біля краю стола.",
            "Направ промінь світла через склянку на аркуш.",
            "Посунь аркуш, поки не з’явиться веселка."
        ],
        "safety_note": "Не дивись прямо у джерело світла.",
        "image": "images/home_rainbow.png",
        "duration": 10,
        "age_range": "5+",
        "level": "дуже легко",
    },
    "magnet-fish": {
        "slug": "magnet-fish",
        "title": "Магнітний риболов",
        "emoji": "🧲",
        "summary": "Ловимо скріпки магнітом і розбираємось із силами.",
        "materials": ["магніт", "скріпки", "мотузочка", "паличка"],
        "steps": [
            "Прив’яжи мотузку до палички.",
            "До кінця мотузки прикріпи магніт.",
            "Збери “рибу” зі скріпок і лови!"
        ],
        "safety_note": "Тримай магніт подалі від електроніки.",
        "image": "images/magnet_fish.png",
        "duration": 15,
        "age_range": "6+",
        "level": "легко",
    },
    "balloon-rocket": {
        "slug": "balloon-rocket",
        "title": "Ракета на нитці",
        "emoji": "🎈",
        "summary": "Повітря тікає — ракета летить!",
        "materials": ["повітряна кулька", "нитка 2–3 м", "соломинка", "скотч"],
        "steps": [
            "Протягни нитку крізь соломинку та закріпи її між двома точками.",
            "Наклей кульку на соломинку скотчем.",
            "Надуйте кульку, затисни отвір і відпусти!"
        ],
        "safety_note": "Не направляй ракету в обличчя людей.",
        "image": "images/balloon_rocket.png",
        "duration": 10,
        "age_range": "6+",
        "level": "легко",
    },
    "gravity-drop": {
        "slug": "gravity-drop",
        "title": "Сила тяжіння в дії",
        "emoji": "🌍",
        "summary": "Що впаде швидше — м’яч чи ложка? Досліджуємо силу тяжіння!",
        "materials": ["м’яч", "ложка", "стіл або стілець"],
        "steps": [
            "Підніми м’яч і ложку.",
            "Відпусти їх одночасно.",
            "Подивись, як обидва падають — це сила тяжіння!"
        ],
        "safety_note": "Слідкуй, щоб ніщо не впало на ногу.",
        "image": "images/gravity_drop.png",
        "duration": 5,
        "age_range": "5+",
        "level": "дуже легко",
    },

    "mass-guess": {
        "slug": "mass-guess",
        "title": "Вгадай масу",
        "emoji": "⚖️",
        "summary": "Гра: здогадайся, що важче — яблуко чи книга?",
        "materials": ["яблуко", "книга", "ваги (за наявності)"],
        "steps": [
            "Візьми два предмети.",
            "Відчуй у руках, що важче.",
            "Перевір на вагах або обговори результат."
        ],
        "safety_note": "Не бери надто важких предметів.",
        "image": "images/mass_guess.png",
        "duration": 10,
        "age_range": "6+",
        "level": "легко",
    },

    "volume-pour": {
        "slug": "volume-pour",
        "title": "Скільки води?",
        "emoji": "🧪",
        "summary": "Порівнюємо об’єм: склянка, чашка, банка — в якій більше?",
        "materials": ["вода", "склянка", "чашка", "банка", "мірний стакан (за бажанням)"],
        "steps": [
            "Налий воду у склянку, чашку і банку.",
            "Порівняй рівень води.",
            "При бажанні — виміряй об’єм мірним стаканом."
        ],
        "safety_note": "Обережно з водою, щоб не розлити.",
        "image": "images/volume_pour.png",
        "duration": 10,
        "age_range": "6+",
        "level": "легко",
    },

    "find-physics": {
        "slug": "find-physics",
        "title": "Знайди фізику навколо",
        "emoji": "🔍",
        "summary": "Дивимось навколо — і шукаємо фізику в повсякденному житті.",
        "materials": ["предмети з дому або класу"],
        "steps": [
            "Озирнись навколо.",
            "Знайди 3 речі, де є фізика (наприклад, магніт на холодильнику, світло, яке вмикається).",
            "Обговори, як це пов’язано з фізикою."
        ],
        "safety_note": "Не торкайся небезпечних приладів.",
        "image": "images/find_physics.png",
        "duration": 7,
        "age_range": "5+",
        "level": "дуже легко",
    },
    "volume-water-amount": {
        "slug": "volume-water-amount",
        "title": "Скільки води?",
        "emoji": "💧",
        "summary": "Переливаємо воду у різні посудини та порівнюємо об’єм.",
        "materials": ["пляшка з водою", "склянка", "чашка", "банка"],
        "steps": [
            "Наповни пляшку водою.",
            "Перелий воду по черзі у склянку, чашку, банку.",
            "Подивись, у чому води більше або менше.",
            "Обговоріть, що таке об’єм і як його видно."
        ],
        "safety_note": "Будь обережним з водою, щоб не розлити.",
        "image": "images/volume_water_amount.png",
        "duration": 10,
        "age_range": "6+",
        "level": "легко",
    },

    "volume-shape-trick": {
        "slug": "volume-shape-trick",
        "title": "Одна вода — різні посудини",
        "emoji": "🥛",
        "summary": "Порівнюємо, як однакова кількість води виглядає по-різному.",
        "materials": ["мірна склянка (200 мл)", "вузька склянка", "широка чаша"],
        "steps": [
            "Налий 200 мл води у мірну склянку.",
            "Перелий її у вузьку склянку — запитай: «У якій більше?»",
            "Тепер перелий у широку чашу — знову запитай.",
            "Поясни, що об’єм не змінився, хоча форма — інша."
        ],
        "safety_note": "Став посуд на рівну поверхню, щоб вода не розлилась.",
        "image": "images/volume_shape_trick.png",
        "duration": 12,
        "age_range": "6+",
        "level": "легко",
    }
        "phone-string": {
        "slug": "telefon-na-nytci",
        "title": "Телефон на нитці",
        "emoji": "📞🧵",
        "summary": "Паперові або пластикові стаканчики + нитка + гудзики або скріпки",
        "materials": ["стаканчики", "нитка 2-3 метри, можна і довшу", "два гудзики або скріпки, щоб прикріпити нитку до стаканчиків", "гарний настрій"],
        "steps": [
            "Підготувати нитку необхідної довжини.",
            "В дні стаканчиків зробити отвори за допомогою голки і просунути в них нитку.",
            "Закріпити нитку на дні стаканчиків за допомогою гудзиків або скріпок."
            "Двоє дітей відходять на достатню відстань для того щоб нитка натягнулася, але не рвалася."
            "Один говорить у стаканчик, а інший підносить свій стаканчик до вуха і слухає."
        ],
        "safety_note": "Обережно, щоб не вколотися голкою.",
        "image": "images/phone.png",
        "duration": 10,
        "age_range": "5+",
        "level": "дуже легко"
    },
}



# ---- Список експериментів ----
def experiments_list(request):
    items = list(EXPERIMENTS.values())
    random.shuffle(items)
    return render(request, "experiments/experiments.html", {"experiments": items})

# ---- Менеджер експериментів (stub UI) ----
@require_http_methods(["GET"])
def experiments_manage(request):
    return render(request, "experiments/experiments_manage.html", {
        "count": len(EXPERIMENTS),
    })

# ---- Швидке додавання (stub форма) ----
@require_http_methods(["GET", "POST"])
def experiments_quick_add(request):
    if request.method == "POST":
        # Стабуємо "збереження": просто редірект на список (реальне збереження додаси потім)
        return redirect("experiments:experiments")
    return render(request, "experiments/experiments_quick_add.html")

# ---- Випадковий експеримент ----
def experiment_random(request):
    slug = random.choice(list(EXPERIMENTS.keys()))
    return redirect("experiments:experiments_detail_static", slug=slug)

# ---- Детальна сторінка (статичні дані з EXPERIMENTS) ----
class ExperimentDetailView(TemplateView):
    template_name = "experiments/experiments_detail_static.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slug = kwargs.get("slug")
        exp = EXPERIMENTS.get(slug)
        if not exp:
            raise Http404("Експеримент не знайдено")
        ctx["exp"] = exp
        return ctx


def sound_lesson(request):
    return None