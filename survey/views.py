from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import *
from .forms import *
from django.urls import reverse
import numpy as np
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
  if 'interests_post' not in request.session:  # interests were not provided yet, redirect to interests view
    return HttpResponseRedirect(reverse('interests'))
  elif 'skills_post' not in request.session:  # skills were not provided yet, redirect to skills view
    return HttpResponseRedirect(reverse('skills'))
  else:
    if request.method == 'POST':
      request.session['results_post'] = request.POST
      return HttpResponseRedirect(reverse('profile_data'))
    else:
      matched_services_list = find_matched_services(request.session, num_services=4)
      context = {'matched_services_list': matched_services_list}
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

        return HttpResponseRedirect(reverse('thank_you_note'))
      else:
        form = ProfileDataForm(restored_form_data)

    else:
      form = ProfileDataForm(restored_form_data)

    context = {'form': form}
    return render(request, 'survey/profile_data.html', context)

def thank_you_note(request):
  context = {
    'thank_you_text': 'Vielen Dank für dein Interesse!',
    'further_note': 'Wir werden uns demnächst mit dir in Kontakt setzen.',
    'time_delay': 7 * 1000 # time delay in ms until redirect
  }
  return render(request, 'survey/thank_you_note.html', context)

class ListProfilesView(LoginRequiredMixin, ListView):
    model = Profile

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

#not a view
def find_matched_services(session, num_services=4):
  assert num_services > 0
  choice_selection_array = choice_array(session)
  service_score_array = score_services(choice_selection_array)
  sorted_services = [service for service, _ in sorted(service_score_array, key=lambda x: x[1], reverse=True)]
  return sorted_services[0:num_services]

#not a view
def score_services(choice_selection_array):
  services = Service.objects.all()

  service_score_array = []
  for service in services:
    service_score = 0
    for choice, selected in choice_selection_array:
      if selected:
        service_score += Service_Choice_Score.objects.get(service=service, choice=choice).score
    service_score += service.service_urgency
    service_score_array.append((service, service_score))

  assert all([isinstance(service, Service) and type(score) == int or type(score) == float for service, score in service_score_array])
  return service_score_array
