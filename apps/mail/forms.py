from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Email, Reply
from django.conf import settings
from apps.users.models import CustomUser


class EmailComposeForm(forms.ModelForm):
    recipient = forms.EmailField()

    class Meta:
        model = Email
        fields = ['recipient', 'subject', 'body']

        def clean_recipient(self):
            email = self.cleaned_data.get('recipient')
            try:
                recipient = CustomUser.objects.get(email__iexact=email)
            except CustomUser.DoesNotExist:
                raise ValidationError("User with this email does not exist.")
            return recipient


class EmailReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
