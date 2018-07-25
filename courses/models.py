from django.db import models
from django.urls import reverse_lazy

from accounts.models import User
from . import constants
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)

    image = models.ImageField(
        default="course_default.png", blank=True,
        upload_to="courses_images")
    pass_percentage = models.PositiveSmallIntegerField(default=60)

    number_of_test_questions = models.PositiveSmallIntegerField(
        default=10, null=True, blank=True)
    has_random_questions = models.BooleanField(default=True)

    # This is always in minutes.
    duration = models.IntegerField("Duration of quiz in minutes", default=20)

    created_by = models.ForeignKey(User, related_name='created_courses',
                                   on_delete=models.DO_NOTHING)
    modified_by = models.ForeignKey(
        User, related_name="modified_courses",
        blank=True, null=True, on_delete=models.DO_NOTHING)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('courses:detail', args=[self.pk])


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons",
                               on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)


class Resource(models.Model):
    title = models.CharField(max_length=20)
    RESOURCE_TYPES = (
        (constants.PDF, 'PDF'),
        (constants.IMAGES, 'IMAGE'),
        (constants.VIDEO, 'VIDEO'),
        (constants.LINK, "LINK")
    )
    lesson = models.ForeignKey(Lesson, related_name="resources", on_delete=models.DO_NOTHING)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    resource = models.FileField(upload_to="resources")

    def __str__(self):
        return "{course} - {lesson}".format(
            course=self.lesson.course.name,
            lesson=self.lesson.name,
        )


class Question(models.Model):

    # MULTIPLE_ANSWER = 'multiple-answers'

    QUESTION_TYPES = (
        (constants.MULTIPLE_CHOICE, 'Multiple Choice'),
        (constants.FILL_IN_THE_BLANKS, "Fill In The Blanks"),
        # (MULTIPLE_ANSWER, 'Multiple Answers')
    )

    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, related_name='questions',
                               on_delete=models.DO_NOTHING)

    description = models.TextField()
    type = models.CharField(max_length=50, choices=QUESTION_TYPES)

    has_random_answers = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="creating_user",
                                   on_delete=models.DO_NOTHING)

    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="user",
                                    blank=True, null=True,
                                    on_delete=models.DO_NOTHING)
    image = models.ImageField(default="question_default.png",
                              blank=True, upload_to="question_images")

    def __str__(self):
        return "{} ({})".format(self.title, self.course.name)


# question.option_set.all()
# question.options.all()

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options',
                                 on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=50, choices=(
        (constants.TEXT, 'Text'),
        (constants.IMAGES, 'Image'),
    ))
    text = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    # will be used only if 'question.has_random_options' is False
    display_order = models.PositiveIntegerField(default=0)

    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return "{question} - {option} (type)".format(
            question=self.question.title,
            option=self.text,
            type=self.type)


class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name="courses",
                               on_delete=models.DO_NOTHING)

    user = models.ForeignKey(User, related_name="users",
                             on_delete=models.DO_NOTHING)

    marks_secured = models.IntegerField(default=0)
    total_number_of_questions = models.PositiveIntegerField(
        null=True, blank=True)
    questions = models.ManyToManyField(Question)
    attempt_date = models.DateTimeField(auto_now_add=True)
    attempt_status = models.CharField(max_length=50, choices=(
        (constants.DRAFT, "Draft"),  # draft, submitted
        (constants.SUBMITTED, "Submitted"),
    ), default=constants.DRAFT)
    quiz_status = models.CharField(max_length=50, choices=(
        (constants.FAILED, "Failed"),  # draft, submitted
        (constants.PASSED, "Passed"),
        (constants.NOT_ATTEMPTED, "Not Attempted")
    ), default=constants.NOT_ATTEMPTED)

    class Meta:
        verbose_name_plural = 'quizzes'

    def __str__(self):
        return "{} ({})".format(self.user, self.course)


class AttemptedQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="attempted_questions",
                             on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name="attempted_user",
                             on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, related_name="questions",
                                 on_delete=models.DO_NOTHING)
    selected_answer = models.ForeignKey(Option, related_name="options",
                                        on_delete=models.DO_NOTHING,
                                        null=True, blank=True)

    def __str__(self):
        return "{user} - {question} - {option} (type)".format(
            user=self.user.get_full_name() or self.user.email,
            question=self.question.title,
            option=self.selected_answer.text)


class Certifications(models.Model):
    user = models.ForeignKey(User, related_name="certified_user",
                             on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="certified_course",
                               on_delete=models.CASCADE)
    certified_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{user} - {course}".format(
            user=self.user.get_full_name() or self.user.email,
            course=self.course.name)

