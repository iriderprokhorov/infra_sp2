import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    """Модель юзера."""
    bio = models.TextField(
        'Биография',
        max_length=400,
        blank=True,
    )
    email = models.EmailField(
        'email',
        unique=True,
    )
    role = models.CharField(
        'Роль',
        choices=ROLES,
        max_length=20,
        default='user',
    )
    confirmation_code = models.UUIDField(
        'UUID',
        default=uuid.uuid4(),
        max_length=256,
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'
