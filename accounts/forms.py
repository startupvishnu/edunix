from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm

from . import models


class UserCreationForm(AuthUserCreationForm):

    username = forms.EmailField(label='Email', required=True)

    class Meta(AuthUserCreationForm.Meta):
        model = models.User

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['username']
        if email and models.User.objects.filter(email=email).exists():
            self.add_error('username', 'User already exists.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['username']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
