from django import template

register = template.Library()

@register.filter
def index(lst, i):
    return lst[i]
