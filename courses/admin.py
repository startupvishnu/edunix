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
    list_display = ("name", "code", "is_active", "pass_percentage", "created_by", "created_on", "modified_on", "image")
    list_filter = ("name", "pass_percentage", "is_active", "created_on")
    search_fields = ("name", "code")

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
    list_display = ("name", "course")
    list_filter = ("name", "course")
    search_fields = ("course__name", "name")


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    exclude = ['created_by', 'modified_by']
    list_display = ("title", "course", "type", "created_by", "created_on", "modified_on")
    list_filter = ("title", "course", "type", "created_by", "created_on")
    search_fields = ("title", "description")

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
    list_display = ("course", "user", "attempt_status", "total_number_of_questions", "marks_secured", "quiz_status")
    list_filter = ("course", "user", "attempt_status", "quiz_status")
    search_fields = ("course__name", "user__email")

# admin.site.register(models.Certifications)

