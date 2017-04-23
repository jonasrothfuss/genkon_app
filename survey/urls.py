from django.conf.urls import url

from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^interests$', views.interests, name='interests'),
    url(r'^skills$', views.skills, name='skills'),
    url(r'^results$', views.results, name='results'),
]
