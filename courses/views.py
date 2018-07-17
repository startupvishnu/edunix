from django.views import generic
from courses import models


class CourseListView(generic.ListView):
    model = models.Course


class CourseDetailView(generic.DetailView):
    model = models.Course


class CourseQuizView(generic.TemplateView):
    model = models.Course

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.get_fo
        return ctx




