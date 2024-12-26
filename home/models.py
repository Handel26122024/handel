from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.core.validators import FileExtensionValidator

class UserManager(BaseUserManager):
    def create_user(self, phone_number, user_name, password=None):
        """
        Creates and saves a regular user with the given phone number, username, and password.
        """
        if not phone_number:
            raise ValueError('Users must have a phone number')
        user = self.model(phone_number=phone_number, user_name=user_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone_number, user_name, password):
        """
        Creates and saves a staff user with the given phone number, username, and password.
        """
        user = self.create_user(phone_number, user_name, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, user_name, password):
        """
        Creates and saves a superuser with the given phone number, username, and password.
        """
        user = self.create_user(phone_number, user_name, password=password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class UserAuth(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(unique=True)
    user_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_name']

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)

    def get_full_name(self):
        return self.user_name

    def get_short_name(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        # Placeholder for custom permission logic
        return True

    def has_module_perms(self, app_label):
        # Placeholder for custom permission logic
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin








class Profile(models.Model):
    user = models.OneToOneField(UserAuth, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255,null=True, blank=True)
    country = models.CharField(max_length=255,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.user_name}'s profile"

