import string
from random import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from apps.company_heirarchy.models import Department, Role
from .managers import CustomUserManager

# Constants
WEBSITE_DOMAIN = 'example.com'


# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model that uses email as the username field
    and leverages department and role information from related models.
    """
    username = None
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, max_length=255, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """
        Generates an email and saves the user instance.
        """
        if not self.email:
            self.email = self.generate_email()
        super().save(*args, **kwargs)

    def generate_email(self):
        """
        Generates an email address based on user information and department code.
        """
        department_code = self.department.code[:3].lower()
        return f"{self.first_name.lower()}.{self.last_name.lower()}@{department_code}.{WEBSITE_DOMAIN}"

    def get_absolute_url(self) -> str:
        """
        Returns the URL for the user's detail view.
        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Profile(models.Model):
    """
    Profile model associated with a CustomUser, storing additional information.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length=280, blank=True)
    address = models.CharField(max_length=280, blank=True)
    employee_id = models.CharField(max_length=12, unique=True, editable=False)

    # def save(self, *args, **kwargs):
    #     """
    #     Generates an employee ID and saves the profile instance.
    #     """
    #     if not self.employee_id:
    #         dept_code = self.user.department.code[:3].upper()
    #         self.employee_id = f"{dept_code}.{''.join(random.choices(string.digits, k=3))}"
    #     super().save(*args, **kwargs)
