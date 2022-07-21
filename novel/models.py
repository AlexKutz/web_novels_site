from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
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

    def get_absolute_urs(self):
        return reverse('novels', args=[str(self.id)])

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
    title = models.CharField(max_length=64, blank=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    content = models.TextField()
    createrd_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.novel} / {self.title} / {self.number}'


@receiver(post_save, sender=Novel)
def update_tag_counter(sender, instance, created, **kwargs):
    count = Tag.objects.annotate(Count('novel'))
    print('work')
    for item in count:
        tag = Tag.objects.get(name=item.name)
        tag.count = item.novel__count
        tag.save()


post_save.connect(update_tag_counter, sender=Novel)


class UserBookShelfBook(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def _get_timesince(self):
        return fixtimesince(timesince(self.created_on, time_strings=TIME_STRINGS, depth=1))

    def _get_total_likes(self):
        return self.likes.users.count()

    time_from_upload = property(_get_timesince)
    totalLikes = property(_get_total_likes)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text[:20], self.user)


class CommentLike(models.Model):
    comment = models.OneToOneField(Comment, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments')

    def __str__(self):
        return 'Comment id {}'.format(self.comment)


class Userip(models.Model):
    ip = models.CharField(verbose_name='Айпи адрес', max_length=30)  # айпи адрес
    count = models.IntegerField(verbose_name="Визиты", default=0)  # Ip посещения

    class Meta:
        verbose_name = "Доступ к информации о пользователе"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"${self.ip} | соединения ({self.count})"


# Всего посещений сайта
class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name="Всего посещений сайта", default=0)  # Всего посещений сайта

    class Meta:
        verbose_name = "Всего посещений сайта"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)


# Статистика посещений за один день
class DayNumber(models.Model):
    day = models.DateField(verbose_name='свидание', default=timezone.now)
    count = models.IntegerField(verbose_name="Количество посещений сайта", default=0)  # Всего посещений сайта

    class Meta:
        verbose_name = "Статистика ежедневных посещений сайта"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)
