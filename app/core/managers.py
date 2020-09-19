from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """Creates and saves a new user"""
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
