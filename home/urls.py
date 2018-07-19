from django.urls import path

from courses.views import CourseListView
from . import views

app_name = 'home'

urlpatterns = [
    path('', CourseListView.as_view(), name='home'),
]
