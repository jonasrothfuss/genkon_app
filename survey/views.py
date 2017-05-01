from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.urls import reverse
from pprint import pprint


def index(request):
  context = {}
  return render(request, 'survey/index.html', context)

def interests(request):
  if request.method == 'POST':
    form = InterestsForm(request.POST)
    if form.is_valid():
      request.session['interests_post'] = request.POST
      return HttpResponseRedirect(reverse('skills'))
    else:
      form = InterestsForm()

  else:
    form = InterestsForm()

  context = {'form': form}
  return render(request, 'survey/interests.html', context)

def skills(request, num_selectors_skills1=3):
  question1 = Question.objects.get(question_identifier="skills1")
  question2 = Question.objects.get(question_identifier="skills2")

  if request.method == 'POST':
    form1 = SkillsForm1(request.POST, num_selectors=num_selectors_skills1)
    form2 = SkillsForm2(request.POST)
    if form1.is_valid() and form2.is_valid():
      request.session['skills_post'] = request.POST
      return HttpResponseRedirect(reverse('results'))
    else:
      form1 = SkillsForm1(num_selectors=num_selectors_skills1)
      form2 = SkillsForm2()

  else:
    form1 = SkillsForm1(num_selectors=num_selectors_skills1)
    form2 = SkillsForm2()

  context = {'form1': form1, 'form2': form2, 'question1': question1, 'question2': question2}
  return render(request, 'survey/skills.html', context)

def results(request):
  print(request.session['interests_post'])
  print(request.session['skills_post'])

  matched_services_list = Service.objects.all()[:4]
  context = {'matched_services_list':  matched_services_list}
  return render(request, 'survey/results.html', context)

def profile_data(request):
  if request.method == 'POST':
    form = ProfileDataForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('results'))
    else:
      form = ProfileDataForm()

  else:
    form = ProfileDataForm()

  context = {'form': form}
  return render(request, 'survey/profile_data.html', context)
