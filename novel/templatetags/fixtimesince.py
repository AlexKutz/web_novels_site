from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
REPLACE_TIME = [5, 6, 7, ] + [number for number in range(10, 370, 10)]
REPLACE_STRING = {
    "минуты": "минут",
    "часа": "часов",
    "дня": "дней",
    "недели": "недель",
    "месяца": "месяцев",
    "года": "лет",
}


@register.filter
@stringfilter
def fixtimesince(value, delimiter=None):
    if value in (None, ''):
        return ''
    if int(value[:2]) in REPLACE_TIME:
        for key, val in REPLACE_STRING.items():
            value = value.replace(key, val)
    return value


fixtimesince.is_safe = True
