from django.shortcuts import render

def index(request):
  context = {}
  return render(request, 'survey/index.html', context)

def interests(request):
  context = {}
  return render(request, 'survey/interests.html', context)

def skills(request):
  context = {}
  return render(request, 'survey/skills.html', context)
