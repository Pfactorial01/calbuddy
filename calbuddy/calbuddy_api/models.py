from __future__ import unicode_literals
from typing import Optional

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    daily_calorie_mark = models.IntegerField(_("daily calorie mark"), default=0)
    date_joined = models.DateField(_("date joined"), auto_now_add=True)
    is_staff = models.BooleanField(_("staff status"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_daily_calorie_mark(self):
        return self.daily_calorie_mark

    def set_daily_calorie_mark(self, new_mark):
        self.daily_calorie_mark = new_mark


class Meal(models.Model):
    date = models.DateField(_("date"), auto_now_add=True)
    time = models.TimeField(_("time"), auto_now_add=True)
    name = models.CharField(_("name"), max_length=30)
    ingredients = models.CharField(_("ingredients"), max_length=200)
    calories = models.IntegerField(_("calories"), default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    within_calorie_limit = models.BooleanField(_("within calorie limit"), default=True)


class Day(models.Model):
    date = models.DateField(_("date"), auto_now_add=True)
    calories_consumed = models.IntegerField(_("calories consumed"), default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
