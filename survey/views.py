from django.shortcuts import render
from .models import *

def index(request):
  context = {}
  return render(request, 'survey/index.html', context)

def interests(request):
  context = {}
  return render(request, 'survey/interests.html', context)

def skills(request):
  context = {}
  return render(request, 'survey/skills.html', context)

def results(request):
  matched_services_list = Service.objects.all()
  context = {'matched_services_list':  matched_services_list}
  return render(request, 'survey/results.html', context)
