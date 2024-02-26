from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a new user with the given email and password.

        Args:
            email: The email address of the user.
            password: The password of the user.
            **extra_fields: Optional keyword arguments for user creation.

        Returns:
            A new `CustomUser` instance.

        Raises:
            ValueError: If the email is blank or None.
        """
        if not email:
            raise ValueError(_("The email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.

        Args:
            email: The email address of the superuser.
            password: The password of the superuser.
            **extra_fields: Optional keyword arguments for superuser creation.

        Returns:
            A new `CustomUser` instance with superuser permissions.

        Raises:
            ValueError: If the email is blank or None.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
