from django.contrib import admin
from .models import *


class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3


class QuestionAdmin(admin.ModelAdmin):
  fields = ['question_text', 'question_type']
  inlines = [ChoiceInline]


class ProfileChoiceAdmin(admin.TabularInline):
  model = Profile_Choice_Selection
  extra = 0

class ProfileAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['date_posted','first_name','last_name']}),
    ('Contact Details', {'fields': ['email', 'phone_number']}),
    ('Address', {'fields': ['street', 'zip_code', 'city']}),
    ('Additional Information', {'fields': ['occupation','message']}),
  ]
  inlines = [ProfileChoiceAdmin]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Service)
admin.site.register(Profile_Choice_Selection)
admin.site.register(Service_Choice_Score)