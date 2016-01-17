from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	# ex: /polls/5/
	url(r'^(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='details'),
	# ex: /polls/5/results
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
	# ex: /polls/5/vote
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
	# ex: /polls/all
	url(r'all/$', views.FullView.as_view(), name='all'),
	# ex: /polls/2/update
	url(r'^(?P<pk>[0-9]+)/update/$', views.Update.as_view(), name='update'),
	# ex: /polls/5/addchoice
	url(r'^(?P<question_id>[0-9]+)/addchoice/$', views.addchoice, name='addchoice'),
]