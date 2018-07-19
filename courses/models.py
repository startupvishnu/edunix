from django.db import models
from django.urls import reverse_lazy

from accounts.models import User
from .constants import *
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, related_name="modified_courses",
        blank=True, null=True, on_delete=models.DO_NOTHING)

    created_by = models.ForeignKey(User, related_name='created_courses',
                                   on_delete=models.DO_NOTHING)
    image = models.ImageField(
        default="course_default.png", blank=True,
        upload_to="courses_images")
    pass_percentage = models.PositiveSmallIntegerField(default=60)
    number_of_test_questions = models.PositiveSmallIntegerField(
        default=10, null=True, blank=True)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse_lazy('courses:detail', args=[self.pk])


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons",
                               on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)


class Resource(models.Model):

    RESOURCE_TYPES = (
        (PDF, 'PDF'),
        (IMAGES, 'IMAGE'),
        (VIDEO, 'VIDEO'),
        (LINK, "LINK")
    )
    lesson = models.ForeignKey(Lesson, related_name="resources", on_delete=models.DO_NOTHING)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    resource = models.FileField(upload_to="resources")


class Question(models.Model):

    #MULTIPLE_ANSWER = 'multiple-answers'

    QUESTION_TYPES = (
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (FILL_IN_THE_BLANKS, "Fill In The Blanks"),
        #(MULTIPLE_ANSWER, 'Multiple Answers')
    )

    course = models.ForeignKey(Course, related_name='questions', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    text_answer = models.CharField(max_length=100)
    is_random = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="creating_user", on_delete=models.DO_NOTHING)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="user", blank=True, null=True, on_delete=models.DO_NOTHING)
    image = models.ImageField(default="question_default.png", blank=True,upload_to="question_images")


# question.option_set.all()
# question.options.all()

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=50, choices=(
        (TEXT, 'Text'),
        (IMAGES, 'Image'),
    ))
    text = models.CharField(max_length=100)
    image = models.ImageField()

    is_answer = models.BooleanField(default=False)
    is_random = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)


class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name="courses", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name="users", on_delete=models.DO_NOTHING)
    marks_secured = models.IntegerField(default=0)
    total_number_of_questions = models.PositiveIntegerField(null=True, blank=True)
    questions = models.ManyToManyField(Question)
    attempt_date = models.DateTimeField(auto_now_add=True)
    attempt_status = models.CharField(max_length=50, choices=(
        (DRAFT, "Draft"),  # draft, submitted
        (SUBMITTED, "Submitted"),
    ), default=DRAFT)
    quiz_status = models.CharField(max_length=50, choices=(
        (FAILED, "Failed"),  # draft, submitted
        (PASSED, "Passed"),
        (NOT_ATTEMPTED, "Not Attempted")
    ), default=NOT_ATTEMPTED)


class AttemptedQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="attempted_questions", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name="attempted_user",on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, related_name="questions", on_delete=models.DO_NOTHING)
    selected_answer = models.ForeignKey(Option, related_name="options", on_delete=models.DO_NOTHING, null=True, blank=True)


class Certifications(models.Model):
    user = models.ForeignKey(User, related_name="certified_user", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="certified_course", on_delete=models.CASCADE)
    certified_on = models.DateTimeField(auto_now_add=True)