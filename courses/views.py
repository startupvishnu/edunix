import copy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from courses import forms
from courses import models
from courses import utils


class CourseListView(generic.ListView):
    model = models.Course


class ResourceListView(generic.ListView):
    model = models.Resource

    def get_queryset(self):
        lesson = models.Lesson.objects.get(id=self.kwargs['pk'])
        return models.Resource.objects.filter(lesson=lesson)


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Course
    login_url = "login"


class CourseQuizView(LoginRequiredMixin, generic.FormView):
    template_name = 'courses/course_quiz.html'
    login_url = "login"
    form_class = forms.QuizModelForm
    quiz = None

    def get_quiz_object(self):
        if self.quiz:
            return self.quiz

        course = get_object_or_404(models.Course,
                                   pk=self.kwargs.get('course_id'))
        self.quiz = utils.get_quiz(self.request.user, course)
        return self.quiz

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'instance': self.get_quiz_object()
        })
        return kwargs

    # def get_form(self, form_class=None):
    #     if self.form:
    #         return self.form
    #     return forms.QuizModelForm(instance=self.get_quiz_object())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form': self.get_form(),
            'object': self.quiz,
        })
        return ctx

    def get_success_url(self):
        return reverse_lazy('courses:detail', args=[self.quiz.course.pk])

    def form_valid(self, form):
        utils.submit_the_quiz(self.get_quiz_object())
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     import ipdb; ipdb.set_trace()
    #     return self.get(request, *args, **kwargs)



