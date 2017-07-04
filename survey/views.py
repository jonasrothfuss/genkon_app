from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import numpy as np
import math
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
  question3 = Question.objects.get(question_identifier="skills3")

  if 'interests_post' in request.session: #assure that interests have been provided
    if request.method == 'POST':
      form1 = SkillsForm1(request.POST, num_selectors=num_selectors_skills1)
      form2 = SkillsForm2(request.POST)
      form3 = SkillsForm3(request.POST)
      if form1.is_valid() and form2.is_valid() and form3.is_valid():
        request.session['skills_post'] = request.POST
        return HttpResponseRedirect(reverse('results'))
      else:
        form1, form2, form3 = setup_skills_forms(request, num_selectors_skills1)
    else:
      form1, form2, form3 = setup_skills_forms(request, num_selectors_skills1)

    context = {'form1': form1, 'form2': form2, 'form3': form3, 'question1': question1, 'question2': question2, 'question3': question3}
    return render(request, 'survey/skills.html', context)

  else: #interests were not provided yet, redirect to interests view
    return HttpResponseRedirect(reverse('interests'))

def results(request):
  num_services_in_db = len(Service.objects.all())

  if 'interests_post' not in request.session:  # interests were not provided yet, redirect to interests view
    return HttpResponseRedirect(reverse('interests'))
  elif 'skills_post' not in request.session:  # skills were not provided yet, redirect to skills view
    return HttpResponseRedirect(reverse('skills'))
  else:
    if request.method == 'POST':
      request.session['results_post'] = request.POST
      return HttpResponseRedirect(reverse('profile_data'))
    else:
      if 'num_services' in request.GET:
        num_services = min(int(request.GET['num_services']), num_services_in_db)
      else:
        num_services = 4

      num_services_extend = num_services + 4
      matched_services_list = find_matched_services(request.session, num_services=num_services)
      context = {'matched_services_list': matched_services_list, 'num_services': num_services_extend}
      return render(request, 'survey/results.html', context)

def profile_data(request):
  error_message = ""
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
      request.session['profile_post'] = request.POST
      form = ProfileDataForm(request.POST)
      if form.is_valid():
        safe_all_forms(request.session)
        clear_session(request)
        return HttpResponseRedirect(reverse('thank_you_note'))
      else:
        error_message = "Bitte gib eine korrekte E-Mail Adresse an."
        form = ProfileDataForm(request.POST)

    else:
       if 'empty_profile' in request.GET and int(request.GET['empty_profile'])==1: #user wants to skip the form --> redirect to skip-form
        return HttpResponseRedirect(reverse('skip'))
       else:
        form = ProfileDataForm(restored_form_data)

    if 'results_post' in request.session:
      title = 'Möchtest Du eine unverbindliche Anfrage starten?'
    else:
      title = 'Bist du dennoch interessiert Dich beim DRK einzubringen?'

    context = {'form': form, 'title': title, 'error_message': error_message}
    return render(request, 'survey/profile_data.html', context)


def skip(request):
  error_message = ""
  """ Check if skill and interest form data is stored in session """
  if 'interests_post' not in request.session:  # interests were not provided yet, redirect to interests view
    return HttpResponseRedirect(reverse('interests'))
  elif 'skills_post' not in request.session:  # skills were not provided yet, redirect to skills view
    return HttpResponseRedirect(reverse('skills'))
  else:  # interests and skills are provided --> proceed with profile data

    if 'profile_post' in request.session:
      restored_form_data = request.session['profile_post']
    else:
      restored_form_data = {}

    if request.method == 'POST':
      request.session['profile_post'] = request.POST
      form = SkipForm(request.POST)
      if form.is_valid():
        safe_all_forms(request.session, skip_profile=True)
        clear_session(request)
        return HttpResponseRedirect(reverse('thank_you_note'))
      else:
        error_message = "Bitte gib eine korrekte E-Mail Adresse an."
        form = SkipForm(request.POST)

    else:
      if 'empty_profile' in request.GET and int(
              request.GET['empty_profile']) == 1:  # user also wants to skip the form --> store survey data with dummy data
        safe_all_forms(request.session, empty_profile=True)
        clear_session(request)
        return HttpResponseRedirect(reverse('thank_you_note') + "?submit=0")
      else:
        form = SkipForm(restored_form_data)

    context = {'form': form, 'error_message': error_message}
    return render(request, 'survey/skip.html', context)


def thank_you_note(request):
  if 'submit' in request.GET:
    context = {
      'thank_you_text': 'Vielen Dank für dein Interesse!',
      'further_note': '',
      'time_delay': 7 * 1000  # time delay in ms until redirect
    }
  else:
    context = {
      'thank_you_text': 'Vielen Dank für dein Interesse!',
      'further_note': 'Wir werden uns demnächst mit dir in Kontakt setzen.',
      'time_delay': 7 * 1000 # time delay in ms until redirect
    }
  return render(request, 'survey/thank_you_note.html', context)

""" Internal Profile List Views"""

@login_required
def profile_list(request):   #TODO Kompatibel mit Class ListProfilesView machen
  activeprofiles = Profile.objects.all().filter(deleted=False) #Profile(deleted=True)
  context = {'activeprofiles': activeprofiles}
  return render(request, 'survey/profile_list.html', context)

@login_required
def delete_profile(request):
    profile_id = request.GET['selected_profile']
    profile = Profile.objects.get(pk=profile_id)
    profile.deleted = True
    profile.save()
    return HttpResponseRedirect(reverse('profile_list'))

@login_required
def profile_detail(request):
  if request.method == 'POST':
    try:
      selected_profile_pk = request.GET['selected_profile']
      model, created = Profile.objects.get_or_create(pk=selected_profile_pk)
      form = ProfileDataEditForm(request.POST, instance=model)
      if form.is_valid():
        form.save()
        selected_profile = Profile.objects.get(pk=selected_profile_pk)
        form = ProfileDataEditForm(instance=selected_profile)
        context = {'form': form, 'selected_profile': selected_profile, 'success_message': 'Steckbrief wurde gespeichert.'}
        return render(request, 'survey/profile_detail.html', context)
      else:
        selected_profile = Profile.objects.get(pk=selected_profile_pk)
        form = ProfileDataEditForm(instance=selected_profile)
        context = {'form': form, 'selected_profile': selected_profile, 'error_message': 'Profildaten konnten nicht gespeichert werden.'}
        return render(request, 'survey/profile_detail.html', context)

    except:
      return HttpResponseRedirect(reverse('profile_list'))
  else: #GET REQUEST
    try:
     selected_profile_pk = request.GET['selected_profile']
     selected_profile = Profile.objects.get(pk=selected_profile_pk)
     form = ProfileDataEditForm(instance=selected_profile)
    except:
      return HttpResponseRedirect(reverse('profile_list'))

    context = {'form': form, 'selected_profile': selected_profile}
    return render(request, 'survey/profile_detail.html', context)

@login_required
def profile_new(request):
  if request.method == 'POST':
    try:
      form = NewProfileForm(request.POST)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('profile_list'))
      else:
        context = {'form': form, 'error_message': 'Der neue Helfer konnte nicht gespeichert werden.'}
        return render(request, 'survey/profile_new.html', context)

    except:
      return HttpResponseRedirect(reverse('profile_list'))
  else: #GET REQUEST
    try:
      form = NewProfileForm()
    except:
      return HttpResponseRedirect(reverse('profile_list'))
    context = {'form': form}
    return render(request, 'survey/profile_new.html', context)

@login_required
def scores(request):
    scores = Service_Choice_Score.objects.all()
    context = {'allscore': scores}
    return render(request, 'survey/scores.html', context)

@login_required
def profile_detail_csv(request):
  selected_profile_pk = request.GET['selected_profile']
  selected_profile = Profile.objects.get(pk=selected_profile_pk)
  # Create the HttpResponse object with the appropriate CSV header.
  csv_string = Profile.get_df(selected_profile=selected_profile_pk, empty_profiles=False).to_csv()
  response = HttpResponse(csv_string, content_type='text/csv')
  filename = 'attachment; filename= "' + selected_profile.first_name + '_' + selected_profile.last_name + '.csv"'
  response['Content-Disposition'] = filename
  return response

@login_required
def profile_csv(request):
  # Create the HttpResponse object with the appropriate CSV header.
  csv_string = Profile.get_df().to_csv()
  response = HttpResponse(csv_string, content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="Helferliste.csv"'
  return response

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
    form3 = SkillsForm3(restored_form_data)
  else:
    form1 = SkillsForm1(num_selectors=num_selectors_skills1)
    form2 = SkillsForm2()
    form3 = SkillsForm3()
  return form1, form2, form3

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
