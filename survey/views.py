from django.shortcuts import render
from .models import *

def index(request):
  context = {}
  return render(request, 'survey/index.html', context)

def interests(request):
  context = {}
  return render(request, 'survey/interests.html', context)

def skills(request):
  question1 = Question.objects.get(question_identifier="skills1")
  question2 = Question.objects.get(question_identifier="skills2")
  choices1 = question1.get_choices()
  choices2 = question2.get_choices()
  number_of_dropdown_skills1 = 3
  assert len(choices1) > 0 and len(choices2) > 0

  context = {'question1': question1, 'choices1': choices1, 'question2': question2,
             'choices2': choices2, 'dropdown_iterator_skills1': range(number_of_dropdown_skills1)}
  return render(request, 'survey/skills.html', context)

def results(request):
  matched_services_list = Service.objects.all()[:4]
  context = {'matched_services_list':  matched_services_list}
  return render(request, 'survey/results.html', context)
