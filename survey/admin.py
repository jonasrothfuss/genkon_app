from django.contrib import admin
from .models import *


class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3


class QuestionAdmin(admin.ModelAdmin):
  fields = ['question_text', 'question_type']
  inlines = [ChoiceInline]

class ProfileAdmin(admin.ModelAdmin):
  pass



admin.site.register(Question, QuestionAdmin)
admin.site.register(Profile)
admin.site.register(Service)