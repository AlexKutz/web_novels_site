from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


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
    createrd_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    description = models.CharField(max_length=900, blank=True)

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
    content = models.TextField()
    createrd_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.novel} / {self.title}'
