from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.urls import reverse
from pprint import pprint

""" VIEWS """

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

    if 'interests_post' in request.session.keys():
      form = InterestsForm(request.session['interests_post'])
    else:
      form = InterestsForm()

  context = {'form': form}
  return render(request, 'survey/interests.html', context)

def skills(request, num_selectors_skills1=3):
  question1 = Question.objects.get(question_identifier="skills1")
  question2 = Question.objects.get(question_identifier="skills2")

  if 'interests_post' in request.session: #assure that interests have been provided
    if request.method == 'POST':
      form1 = SkillsForm1(request.POST, num_selectors=num_selectors_skills1)
      form2 = SkillsForm2(request.POST)
      if form1.is_valid() and form2.is_valid():
        request.session['skills_post'] = request.POST
        return HttpResponseRedirect(reverse('results'))
      else:
        form1, form2 = setup_skills_forms(request, num_selectors_skills1)
    else:
      form1, form2 = setup_skills_forms(request, num_selectors_skills1)

    context = {'form1': form1, 'form2': form2, 'question1': question1, 'question2': question2}
    return render(request, 'survey/skills.html', context)

  else: #interests were not provided yet, redirect to interests view
    return HttpResponseRedirect(reverse('interests'))

def results(request):
  matched_services_list = Service.objects.all()[:4]
  context = {'matched_services_list':  matched_services_list}
  return render(request, 'survey/results.html', context)

def profile_data(request):
  """ Check if skill and interest form data is stored in session """
  if 'interests_post' not in request.session:  #interests were not provided yet, redirect to interests view
    return HttpResponseRedirect(reverse('interests'))
  elif 'skills_post' not in request.session: #skills were not provided yet, redirect to skills view
    return HttpResponseRedirect(reverse('skills'))

  else: #interests and skills are provided --> proceed with profile data

    if 'profile_post' in request.session:
      restored_form_data = request.session['profile_post']
    else:
      restored_form_data = {}

    if request.method == 'POST':
      form = ProfileDataForm(request.POST)
      if form.is_valid():
        request.session['profile_post'] = request.POST

        safe_all_forms(request.session)
        clear_session(request)

        return HttpResponseRedirect(reverse('results'))
      else:
        form = ProfileDataForm(restored_form_data)

    else:
      form = ProfileDataForm(restored_form_data)

    context = {'form': form}
    return render(request, 'survey/profile_data.html', context)


""" HELPER METHODS"""

#not a view
def clear_session(request):
  for sesskey in list(request.session.keys()):
    del request.session[sesskey]

#not a view
def setup_skills_forms(request, num_selectors_skills1):
  if 'skills_post' in request.session:
    restored_form_data = request.session['skills_post']
    form1 = SkillsForm1(restored_form_data, num_selectors=num_selectors_skills1)
    form2 = SkillsForm2(restored_form_data)
  else:
    form1 = SkillsForm1(num_selectors=num_selectors_skills1)
    form2 = SkillsForm2()
  return form1, form2
