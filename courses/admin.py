from django.contrib import admin
from .models import *

# Register your models here.


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]


admin.site.register(Resource)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Quiz)
admin.site.register(AttemptedQuestion)
admin.site.register(Certifications)

