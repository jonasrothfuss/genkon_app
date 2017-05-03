from django.conf.urls import url

from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^interests$', views.interests, name='interests'),
    url(r'^skills$', views.skills, name='skills'),
    url(r'^results$', views.results, name='results'),
    url(r'^profile_data$', views.profile_data, name='profile_data'),
    url(r'^thank_you', views.thank_you_note, name='thank_you_note'),
]
