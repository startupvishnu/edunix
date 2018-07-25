from django.urls import include, path
from . import views

app_name = "courses"

urlpatterns = [
    path('', views.CourseListView.as_view(), name="list"),
    path('<int:pk>', views.CourseDetailView.as_view(), name="detail"),
    path('resources/<int:pk>', views.ResourceListView.as_view(), name="resource_list"),
    path('<int:course_id>/quiz', views.CourseQuizView.as_view(), name="quiz")
]
