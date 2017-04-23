from django.shortcuts import render

def index(request):
  context = {}
  return render(request, 'survey/index.html', context)
