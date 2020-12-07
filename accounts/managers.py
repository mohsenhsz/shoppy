from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, full_name, email, password=None):
        if not email:
            raise ValueError('Users must have an Email address')
        if not full_name:
            raise ValueError('Users must have an Full Name')
        user = self.model(email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, password=None):
        user = self.create_user(full_name, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
