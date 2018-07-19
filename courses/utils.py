import random
from .constants import *
from .models import Quiz, Question


def start_quiz(user, course):
    question_ids = list(course.questions.values_list('id', flat=True))
    quiz_question_ids = random.sample(
        question_ids, course.number_of_test_questions
    )
    quiz = Quiz.objects.create(
        course=course, user=user,
        total_number_of_questions=course.number_of_test_questions,
    )
    quiz.questions.add(*list(Question.objects.filter(
        id__in=quiz_question_ids)))
    return quiz


def get_next_quiz_question(quiz):
    return quiz.questions.exclude(
        id__in=quiz.attempted_questions.values_list('id', flat=True)
    ).order_by('display_order').first()


def attempt_a_quiz_question(quiz, question):
    if quiz.attempted_questions.filter(id=question.id).exists():
        raise Exception("Already Attempted")
    else:
        quiz.attempted_questions.add(question)


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
            quiz.quiz_status = PASSED
        else:
            quiz.quiz_status = FAILED
        quiz.save()





    else:
        raise Exception("Aready submitted")