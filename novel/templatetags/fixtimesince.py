from django import template
from django.template.defaultfilters import stringfilter
from itertools import chain

register = template.Library()

REPLACE_TIME = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] \
               + list(chain.from_iterable((i, i + 5, i + 6, i + 7, i + 8, i + 9) for i in range(20, 60, 10)))

REPLACE_STRING = {
    "минуты": "минут",
    "часа": "часов",
    "дня": "дней",
    "недели": "недель",
    "месяца": "месяцев",
    "года": "лет",
}

REPLACE_STRING1 = {
    "минуты": "минута",
    "часа": "час",
}


@register.filter
@stringfilter
def fixtimesince(value, delimiter=None):
    if value[0] == '0':
        return 'Только что'

    if value in (None, ''):
        return ''
    if int(value[:2]) in [21, 31, 41, 51]:
        for key, val in REPLACE_STRING1.items():
            value = value.replace(key, val)
    if int(value[:2]) in REPLACE_TIME:
        for key, val in REPLACE_STRING.items():
            value = value.replace(key, val)
    return value + ' назад'


fixtimesince.is_safe = True
