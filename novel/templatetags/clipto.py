from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def clipto(value, delimiter=None):
    return value.split(delimiter)[0]
clipto.is_safe = True