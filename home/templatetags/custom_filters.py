from django import template

register = template.Library()

@register.filter
def subtract(value1, value2):
    return value1 - value2
