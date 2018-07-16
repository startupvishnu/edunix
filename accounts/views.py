# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from . import forms
from . import models


class RegistrationView(generic.CreateView):
    model = models.User
    form_class = forms.UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        response = super().form_valid(form)
        messages.success(self.request, 'Successfully Registered. Please login!')
        return response

