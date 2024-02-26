from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=5, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


class Role(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


