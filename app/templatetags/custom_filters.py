"""
Filtros personalizados de templates - Copiado del proyecto original
"""

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Agrega una clase CSS a un widget del formulario."""
    return field.as_widget(attrs={"class": css_class})
