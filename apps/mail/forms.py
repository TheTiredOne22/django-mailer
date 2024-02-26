from django import forms
from django.core.exceptions import ValidationError

from .models import Email
from django.conf import settings

User = settings.AUTH_USER_MODEL


class EmailComposeForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['recipient', 'subject', 'body']

        def clean_recipient(self):
            email = self.cleaned_data.get('recipient')
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise ValidationError("User with this email does not exist.")
            return user
