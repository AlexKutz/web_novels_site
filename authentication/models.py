from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        'username',
        unique=True,
        max_length=32,
        help_text='Required. 32 ASCII characters',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },

    )
    email = models.EmailField(
        'email',
        max_length=255,
        # unique=True,
        blank=True,
    )

    image = models.ImageField(default='defaultUserImage.svg', upload_to='user-images')

    last_login = models.DateTimeField('last login', blank=True, null=True)
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
