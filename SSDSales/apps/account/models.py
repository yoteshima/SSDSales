# -*- coding: utf-8 -*-

import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _



class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(verbose_name=_('user id'),
                primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(verbose_name=_('last name'),
                max_length=10, default=_('saishido'))
    first_name = models.CharField(verbose_name=_('first name'),
                max_length=10, default=_('taro'))
    last_name_kana = models.CharField(verbose_name=_('last name kana'),
                max_length=10, default=_('saishido'))
    first_name_kana = models.CharField(verbose_name=_('first name kana'),
                max_length=10, default=_('taro'))
    tel = models.CharField(verbose_name=_('phone number'),
                max_length=15, blank=True, null=True)
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    icon = models.ImageField(verbose_name=_('icon'),
                upload_to='account/', blank=True, null=True)
    detail = models.TextField(verbose_name=_('user detail'),
                max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(verbose_name=_('created date'),
                blank=True, null=True, default=datetime.now())
    update_date = models.DateTimeField(verbose_name=_('update date'),
                blank=True, null=True)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_auth_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_staff_property(self) -> bool:
        return self.is_admin


    @property
    def is_superuser_property(self) -> bool:
        return self.is_admin


    def __str__(self) -> str:
        return "{} {}".format(
                self.last_name, self.first_name)