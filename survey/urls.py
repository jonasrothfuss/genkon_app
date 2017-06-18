from django.conf.urls import url, include


from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^interests$', views.interests, name='interests'),
    url(r'^skills$', views.skills, name='skills'),
    url(r'^results$', views.results, name='results'),
    url(r'^profile_data$', views.profile_data, name='profile_data'),
    url(r'^thank_you', views.thank_you_note, name='thank_you_note'),
    url(r'^profile_list', views.ListProfilesView.as_view(), name='profile_list'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^profile_csv', views.profile_csv, name='profile_csv'),
    url(r'^profile_detail_csv', views.profile_detail_csv, name='profile_detail_csv'),
    url(r'^profile_detail', views.profile_detail, name='profile_detail'),
    url(r'^profile_new', views.profile_new, name='profile_new'),
    url(r'^delete_profile', views.delete_profile, name='delete_profile'),

]
