from django.contrib import admin
from .models import  *

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Resource)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Quiz)
admin.site.register(AttemptedQuestion)
admin.site.register(Certifications)

