from django.contrib import admin
from .models import Survey, Question, Choice, Submission

# Register your models here.
class QuestionInline(admin.TabularInline):
  model = Question
  show_change_link = True

class ChoiceInline(admin.TabularInline):
  model = Choice


class SurveyAdmin(admin.ModelAdmin):
  inlines = [
    QuestionInline
  ]

class QuestionAdmin(admin.ModelAdmin):
  inlines = [
    ChoiceInline
  ]
  
class SubmissionAdmin(admin.ModelAdmin):
  list_display = ('participant_email', 'status')

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)


# from .models import Survey, Question, Choice, Submission

# class ChoiceInline(admin.TabularInline):
#   model = Choice

# class QuestionAdmin(admin.ModelAdmin):
#   inlines = [
#     ChoiceInline
#   ]

# admin.site.register(Question, QuestionAdmin)