from django.views import generic
from courses import models


class HomeView(generic.ListView):
    template_name = 'home/home.html'
    model = models.Course



