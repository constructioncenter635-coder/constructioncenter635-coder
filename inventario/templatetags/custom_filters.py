from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # Retorna lista vacía si la clave no existe
    return dictionary.get(key, [])
