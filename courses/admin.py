from django.contrib import admin
from . import models

# Register your models here.


class ResourceInline(admin.TabularInline):
    model = models.Resource
    extra = 0


class LessonInline(admin.TabularInline):
    model = models.Lesson
    extra = 0


class QuestionInline(admin.StackedInline):
    model = models.Question
    extra = 0
    # exclude = ['created_by', 'modified_by']


class OptionInline(admin.TabularInline):
    model = models.Option
    extra = 0


class AttemptedQuestionInline(admin.TabularInline):
    model = models.AttemptedQuestion
    extra = 0


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the creator field.
        """
        if obj and not obj.pk:
            obj.created_by = request.user

        if change:
            obj.modified_by = request.user

        obj.save()


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [ResourceInline]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the creator field.
        """
        if obj and not obj.pk:
            obj.created_by = request.user

        if change:
            obj.modified_by = request.user

        obj.save()


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [AttemptedQuestionInline]


# admin.site.register(models.Certifications)

