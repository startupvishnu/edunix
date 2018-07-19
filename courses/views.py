from django.views import generic

from courses import forms
from courses import models
from courses import utils


class CourseListView(generic.ListView):
    model = models.Course


class CourseDetailView(generic.DetailView):
    model = models.Course


class CourseQuizView(generic.DetailView):
    model = models.Course
    quiz = None
    form = None

    def get_form(self):
        if self.form:
            return self.form

        if not self.quiz:
            self.quiz = utils.start_quiz(self.request.user, self.get_object())

        return forms.QuizModelForm(instance=self.quiz)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.get_form()
        return ctx


