from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import ChangePasswordForm, AvatarUpdateForm, CustomUserUpdateForm, CustomProfileUpdateForm
# Create your views here.
from django.views.generic import TemplateView


def account_settings(request):
    profile = request.user.profile
    avatar_form = AvatarUpdateForm(instance=profile)
    profile_form = CustomProfileUpdateForm(instance=profile)
    password_form = ChangePasswordForm(user=request.user)

    if request.method == 'POST':
        if 'avatar_form' in request.POST:
            avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=profile)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, 'Your profile picture has been updated successfully.')
                return redirect('users:account_settings')
        elif 'profile_form' in request.POST:
            profile_form = CustomProfileUpdateForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile information has been updated successfully.')
                return redirect('users:account_settings')
        elif 'password_form' in request.POST:
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                new_password = password_form.cleaned_data['new_password']
                request.user.set_password(new_password)
                request.user.save()
                # It's important to update the session auth hash to prevent the user from being logged out
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('users:account_settings')

    return render(request, 'account/settings.html', {
        'avatar_form': avatar_form,
        'profile_form': profile_form,
        'password_form': password_form
    })
