from django import forms
from django.core.exceptions import ValidationError, FieldDoesNotExist
from .models import Lesson, Exercise

# ---- helpers --------------------------------------------------------------

def has_model_field(model, name: str) -> bool:
    try:
        model._meta.get_field(name)
        return True
    except FieldDoesNotExist:
        return False

def _split_lines(value):
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return [str(x).strip() for x in value if str(x).strip()]
    raw = str(value).replace("\r\n", "\n").split("\n")
    parts = []
    for line in raw:
        line = line.strip()
        if not line:
            continue
        if ";" in line:
            parts.extend([p.strip() for p in line.split(";") if p.strip()])
        else:
            parts.append(line)
    return parts

def _list_or_text_for_model_field(model, field_name, parts):
    if not has_model_field(model, field_name):
        return None
    field = model._meta.get_field(field_name)
    internal = getattr(field, "get_internal_type", lambda: "")()
    if internal in {"JSONField", "ArrayField"}:
        return parts
    return "; ".join(parts)


# ---- Lesson form ----------------------------------------------------------

class LessonForm(forms.ModelForm):
    # Віртуальні поля для зручного вводу (завжди є у формі, але не в моделі)
    materials_input = forms.CharField(
        label="Матеріали (по одному в рядку)",
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "склянка\nліхтарик\nаркуш"}),
        required=False
    )
    steps_input = forms.CharField(
        label="Кроки (по одному в рядку)",
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Постав склянку\nНаправ світло\nЗнайди веселку"}),
        required=False
    )

    class Meta:
        model = Lesson
        fields = "__all__"   # <— жодних невідомих полів тут

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Плейсхолдери/віджети для тих полів, які справді існують у моделі
        if has_model_field(Lesson, "title"):
            self.fields["title"].widget.attrs.setdefault("placeholder", "Домашня веселка")
        if has_model_field(Lesson, "slug"):
            self.fields["slug"].widget.attrs.setdefault("placeholder", "home-rainbow")
        if has_model_field(Lesson, "summary"):
            self.fields["summary"].widget = forms.Textarea(attrs={"rows": 3, "placeholder": "Склянка води + світло = кольори!"})
        if has_model_field(Lesson, "duration"):
            self.fields["duration"].widget = forms.NumberInput(attrs={"min": 1, "step": 1})
        if has_model_field(Lesson, "emoji"):
            self.fields["emoji"].widget.attrs.setdefault("maxlength", 4)
            self.fields["emoji"].widget.attrs.setdefault("placeholder", "🌈")

        # Якщо у моделі є materials/steps — сховаємо їх (бо вводимо через *_input)
        if has_model_field(Lesson, "materials"):
            self.fields["materials"].widget = forms.HiddenInput()
        if has_model_field(Lesson, "steps"):
            self.fields["steps"].widget = forms.HiddenInput()

        # Ініціалізуємо *_input з існуючих значень (якщо такі поля є в моделі)
        if self.instance and self.instance.pk:
            def as_lines(val):
                if isinstance(val, (list, tuple)):
                    return "\n".join([str(x).strip() for x in val if str(x).strip()])
                return str(val or "").replace("; ", "\n").replace(";", "\n")
            if has_model_field(Lesson, "materials"):
                self.fields["materials_input"].initial = as_lines(getattr(self.instance, "materials"))
            if has_model_field(Lesson, "steps"):
                self.fields["steps_input"].initial = as_lines(getattr(self.instance, "steps"))

    def clean(self):
        cleaned = super().clean()

        # Якщо в моделі є відповідні поля — підставляємо туди з віртуальних textarea
        if has_model_field(Lesson, "materials"):
            mats_list = _split_lines(cleaned.get("materials_input"))
            cleaned["materials"] = _list_or_text_for_model_field(Lesson, "materials", mats_list)
        if has_model_field(Lesson, "steps"):
            steps_list = _split_lines(cleaned.get("steps_input"))
            cleaned["steps"] = _list_or_text_for_model_field(Lesson, "steps", steps_list)

        # Базова валідація назви (лише якщо поле існує)
        if has_model_field(Lesson, "title") and not cleaned.get("title"):
            raise ValidationError("Вкажіть назву уроку.")
        return cleaned


# ---- Exercise form --------------------------------------------------------

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "order" in self.fields:
            self.fields["order"].widget = forms.NumberInput(attrs={"min": 0, "step": 1})
        if "title" in self.fields:
            self.fields["title"].widget.attrs.setdefault("placeholder", "Крок 1: Підготовка")
        # підтримка різних назв текстового поля
        for name in ("instructions", "description", "content"):
            if name in self.fields:
                self.fields[name].widget = forms.Textarea(attrs={"rows": 5, "placeholder": "Опис вправи або інструкції"})
                break
