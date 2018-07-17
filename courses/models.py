from django.db import models
from accounts.models import User

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=30)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="modified_courses", on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, related_name='created_courses', on_delete=models.CASCADE)
    image = models.ImageField(default="course_default.png", blank=True, upload_to="courses_images")
    pass_percentage = models.PositiveSmallIntegerField()


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Resource(models.Model):
    RESOURCE_TYPES = (
        ('pdf', 'PDF'),
        ('image', 'IMAGE'),
        ('video', 'VIDEO'),
        ("link", "LINK")
    )
    lesson = models.ForeignKey(Lesson, related_name="resources", on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    resource = models.FileField(upload_to="resources")


class Question(models.Model):
    MULTIPLE_CHOICE = 'multiple-choice'
    FILL_IN_THE_BLANKS = 'fill-in-the-blanks'
    MULTIPLE_ANSWER = 'multiple-answers'

    QUESTION_TYPES = (
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (FILL_IN_THE_BLANKS, "Fill In The Blanks"),
        (MULTIPLE_ANSWER, 'Multiple Answers')
    )

    course = models.ForeignKey(Course, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    text_answer = models.CharField(max_length=100)
    is_random = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="creating_user", on_delete=models.CASCADE)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    image = models.ImageField(default="question_default.png", blank=True,upload_to="question_images")


# question.option_set.all()
# question.options.all()

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=(
        ('text', 'text'),
        ('image', 'image'),
    ))
    text = models.CharField(max_length=100)
    image = models.ImageField()

    is_answer = models.BooleanField(default=False)
    is_random = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)


class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name="courses", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    marks_secured = models.IntegerField()
    questions = models.ManyToManyField(Question)

    attempt_status = models.CharField(max_length=50, choices=(
        ('Draft', "Draft"),  # draft, submitted
        ("Submitted", "Submitted"),
    ), default="Draft")
    quiz_status = models.CharField(max_length=50, choices=(
        ('F', "Failed"),  # draft, submitted
        ("P", "Passed"),
        ("NA", "Not Attempted")
    ), default="NA")


class AttemptedQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="attempted_questions", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="attempted_user",on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="questions", on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Option, related_name="options", on_delete=models.CASCADE, null=True, blank=True)


class Certifications(models.Model):
    user = models.ForeignKey(User, related_name="certified_user", on_delete=models.CASCADE)
    couser = models.ForeignKey(Course, related_name="certified_course", on_delete=models.CASCADE)
    certified_on = models.DateTimeField(auto_now_add=True)