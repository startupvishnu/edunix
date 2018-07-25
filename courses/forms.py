import math

from django import forms

from . import constants
from . import models


class QuizModelForm(forms.ModelForm):

    id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = models.Quiz
        fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:

            for question in instance.questions.iterator():

                field_name = 'question_%s' % question.id

                if question.type == constants.FILL_IN_THE_BLANKS:
                    self.fields[field_name] = forms.CharField(
                        label=question.description)

                elif question.type == constants.MULTIPLE_CHOICE:
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.description,
                        widget=forms.RadioSelect
                    )

                    field_choices = []
                    for option in question.options.iterator():
                        field_choices.append((
                            option.id, option.text
                        ))

                    self.fields[field_name].choices = field_choices

    def clean(self):
        cleaned_data = super().clean()

        questions_data = {key: cleaned_data[key] for key in cleaned_data
                          if key.startswith('question_')}

        question_errors = {}
        score = 0

        for key, value in questions_data.items():

            question = self.instance.questions.get(
                pk=key.split("question_")[-1])

            if question.type == constants.MULTIPLE_CHOICE:
                option = question.options.get(pk=value)
                if option.is_answer:
                    score += 1
                else:
                    question_errors[key] = 'Incorrect Answer'

            elif question.type == constants.FILL_IN_THE_BLANKS:
                answer_option = question.options.filter(is_answer=True).first()

                if answer_option.text.lower() == value.lower():
                    score += 1
                else:
                    question_errors[key] = 'Incorrect Answer'

        attempt_percentage = (
            float(score) / self.instance.course.number_of_test_questions
        ) * 100

        if attempt_percentage < self.instance.course.pass_percentage:
            for question_key, question_error in question_errors.items():
                self.add_error(question_key, question_error)

            self.add_error(
                None, "You have got {}%. You need to get {}% to pass this quiz".format(
                    math.ceil(attempt_percentage),
                    self.instance.course.pass_percentage
                ))

        return cleaned_data


