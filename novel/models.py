from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count
from django.utils.timesince import timesince
from django.utils.translation import ngettext_lazy

from .utils.fixtimesince import fixtimesince
from .utils.number_words_filter import number_words_filter
from django.db.models.signals import post_save

TIME_STRINGS = {
    'year': ngettext_lazy('%(num)d год', '%(num)d года', 'num'),
    'month': ngettext_lazy('%(num)d месяц', '%(num)d месяца', 'num'),
    'week': ngettext_lazy('%(num)d неделя', '%(num)d недели', 'num'),
    'day': ngettext_lazy('%(num)d день', '%(num)d дня', 'num'),
    'hour': ngettext_lazy('%(num)d час', '%(num)d часа', 'num'),
    'minute': ngettext_lazy('%(num)d минута', '%(num)d минуты', 'num'),
}

class Status(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=16)
    abbreviation = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.abbreviation} / {self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-count']

    def __str__(self):
        return self.name


class Novel(models.Model):
    book_image = models.ImageField(upload_to='./novel/book_cover')
    title = models.CharField(max_length=64, unique=True)
    alt_title = models.CharField(
        max_length=64, blank=True, verbose_name="alternative title")
    adult_only = models.BooleanField(default=False)
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    words = models.PositiveIntegerField(
        verbose_name="number of words")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, related_name='novel')
    description = models.CharField(max_length=900, blank=True)

    class Meta:
        ordering = ['-created_at']


    def _get_timesince(self):
        return fixtimesince(timesince(self.created_at, time_strings=TIME_STRINGS, depth=1))

    def _get_num_words_formatted(self):
        return number_words_filter(self.words)

    time_from_upload = property(_get_timesince)
    number_words_formatted = property(_get_num_words_formatted)

    def __str__(self):
        return f'{self.title} / {self.author}'


class Rate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )

    def __str__(self):
        return f'{self.user} / {self.novel} / {self.rate}'


class Chapter(models.Model):
    title = models.CharField(max_length=16, blank=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    content = models.TextField()
    createrd_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.novel} / {self.title}'


def update_tag_counter(sender, instance, created, **kwargs):
    # Update counter in tag model
    count = Tag.objects.annotate(Count('novel'))
    for item in count:
        tag = Tag.objects.get(name=item.name)
        tag.count = item.novel__count
        tag.save()


post_save.connect(update_tag_counter, sender=Novel)


class UserBookshelf(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    novels = models.ManyToManyField(Novel, related_name='bookshelf', blank=True)
