import datetime
import random

from django.utils.timezone import now

from . import constants
from . import models


def start_quiz(user, course):
    question_ids = list(course.questions.values_list('id', flat=True))

    quiz_question_ids = random.sample(
        question_ids, course.number_of_test_questions
    ) if question_ids else []

    quiz = models.Quiz.objects.create(
        course=course, user=user,
        total_number_of_questions=len(quiz_question_ids),
    )
    if quiz_question_ids:
        quiz.questions.add(*list(models.Question.objects.filter(
            id__in=quiz_question_ids)))
    return quiz


def get_quiz(user, course):
    # last active quiz instance time
    start_datetime = now() - datetime.timedelta(minutes=course.duration)
    recently_active_quiz_objects = models.Quiz.objects.exclude(
        attempt_status=constants.SUBMITTED
    ).filter(user=user, course=course, attempt_date__gt=start_datetime)

    if recently_active_quiz_objects.exists():
        return recently_active_quiz_objects.first()

    return start_quiz(user, course)


def get_next_quiz_question(quiz):
    return quiz.questions.exclude(
        id__in=quiz.attempted_questions.values_list('id', flat=True)
    ).order_by('display_order').first()


def attempt_a_quiz_question(user, quiz, question, option):
    if quiz.attempted_questions.filter(question=question).exists():
        raise Exception("Already Attempted")
    else:
        quiz.attempted_questions.create(
            user=user,
            question=question,
            option=option
        )


def submit_the_quiz(quiz):
    if quiz.attempt_status == "Draft":
        score = 0
        for attempt_question in quiz.attempted_questions.all():
            if attempt_question.selected_answer.is_answer:
                score += 1
        marks_secured = (
                float(score) / quiz.total_number_of_questions
        ) * 100

        quiz.attempt_status = 'Submitted'
        if marks_secured > quiz.course.pass_percentage:
            quiz.quiz_status = constants.PASSED
        else:
            quiz.quiz_status = constants.FAILED
        quiz.save()
    else:
        raise Exception("Aready submitted")