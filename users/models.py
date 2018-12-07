from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
import os


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, first_name=None, last_name=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an Email")
        if not password:
            raise ValueError("User must provide a password")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None, first_name=None, last_name=None):
        user = self.create_user(
            email,
            password,
            first_name,
            last_name,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None, first_name=None, last_name=None):
        user = self.create_user(
            email,
            password,
            first_name,
            last_name,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, null=True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


# def get_file_ext(filepath):
#     base_name = os.path.basename(filepath)
#     name, ext = os.path.splitext(base_name)
#     return name, ext


# def upload_image_path(instance, filename):
#     name_ins = str(instance)
#     _, ext = get_file_ext(filename)
#     return "profilepics/{name}{ext}".format(name=name_ins, ext=ext)


