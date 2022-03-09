from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def number_words_filter(value, delimiter=None):

    if len(value) > 6:
        return f'{value[0:len(value) - 6]},{value[len(value) - 6:len(value) - 6 + 2]} млн'
    elif len(value) < 7:
        return f'{value[0:-3]} тыс'
number_words_filter.is_safe = True