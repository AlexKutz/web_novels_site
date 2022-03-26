from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'Имя пользователя',
        unique=True,
        max_length=32,
        help_text='Это значение может содержать до 32 букв, '
         'цифр и символов @/./+/-/_.',
        validators=[username_validator],
        error_messages={
            'unique': "Пользователь с таким именем уже зарегистрирован.",
        },

    )
    email = models.EmailField(
        'Электронная почта',
        help_text='Используют для восстановления доступа к аккаунту.',
        max_length=255,
        # unique=True,
        blank=True,
    )
    is_active_email = models.BooleanField(
        'active email',
        default=False,
        help_text='If user verified email'
    )

    image = models.ImageField(default='./authentication/img/defaultUserImage.svg', upload_to='user-images')

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.username
