from __future__ import annotations

from typing import Optional
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class UserQuerySet(models.QuerySet['User']):
    def active(self) -> models.query.QuerySet[User]:
        return self.filter(status=User.Status.ACTIVE)

    def filter_by_status(self, status: Optional[str]) -> models.query.QuerySet[User]:
        if not status:
            return self
        return self.filter(status=status)


class UserManager(BaseUserManager['User']):
    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def active(self) -> 'models.query.QuerySet[User]':
        return self.get_queryset().active()


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    class Status(models.TextChoices):
        ACTIVE = ('user_status_active', 'Active')
        EMAIL_CONFIRMING = ('user_status_email_confirming', 'Email Confirming')
        DEACTIVATED = ('user_status_deactivated', 'Deactivated')

    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.EMAIL_CONFIRMING,
    )
    email = models.EmailField()
    password = models.CharField(max_length=255, null=True, blank=True)  # type: ignore
    facebook_user_id = models.CharField(max_length=255, null=True, blank=True)

    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        help_text='DjangoAdminにアクセスするための項目です。',
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='システム管理のスタッフかどうか。DjangoAdmin用です。',
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text='システム管理の管理者かどうか。DjangoAdmin用です。',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'users'

    def __str__(self) -> str:
        return self.email

    def is_active(self) -> bool:  # type: ignore
        return self.status == User.Status.ACTIVE


class PostQuerySet(models.QuerySet['Post']):
    def published(self) -> models.query.QuerySet[Post]:
        return self.filter(published_date__lte=timezone.now())


class PostManager(BaseUserManager['Post']):
    def get_queryset(self) -> PostQuerySet:
        return PostQuerySet(self.model, using=self._db)

    def published(self) -> 'models.query.QuerySet[Post]':
        return self.get_queryset().select_related('author').published()


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'posts'

    def __str__(self) -> int:
        return self.title

    @classmethod
    def publish(self) -> None:
        self.published_date = timezone.now()
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    birthday = models.DateField()

    class Meta:
        db_table = 'profiles'

    @classmethod
    def get_user_profile(cls, user: User) -> Profile:
        try:
            user.profile
        except User.profile.RelatedObjectDoesNotExist:  # type: ignore
            raise
