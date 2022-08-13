from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def create_user(self, email: str, passwords: str, **extra):
        if not email:
            raise ValueError(_("Email can not be empty"))
        if not passwords:
            raise ValueError(_("Password can not be empty"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(passwords)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra):
        extra['is_staff'] = True
        extra['is_superuser'] = True
        if not 'is_active' in extra:
            extra['is_active'] = True
        return self.create_user(email, password, **extra)