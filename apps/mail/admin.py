from django.contrib import admin
from .models import Email, UserEmailActions

# Register your models here.


admin.site.register(Email)
admin.site.register(UserEmailActions)
