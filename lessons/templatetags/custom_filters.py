from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Ділить рядок за вказаним роздільником."""
    return [item.strip() for item in value.split(delimiter) if item.strip()]
