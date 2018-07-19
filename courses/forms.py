from django import forms

from . import models


class QuizModelForm(forms.ModelForm):

    class Meta:
        model = models.Quiz
        exclude = []
