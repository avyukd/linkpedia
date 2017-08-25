from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
	url(r'^home/expert/(?P<username>[\w\-]+)$', views.home, name='home'),
	url(r'^home/user/(?P<username>[\w\-]+)$', views.home, name='home'),
	url(r'^viewprofile/(?P<username>[\w\-]+)', views.viewprofile, name='viewprofile'),
	url(r'^addcontent/(?P<username>[\w\-]+)$', views.addcontent, name='addcontent'),
	url(r'^addlink/(?P<username>[\w\-]+)$', views.addlink, name='addlink'),
	url(r'^(?P<id>[0-9]+)$', views.linkinfo, name='linkinfo'),
	url(r'^signupint/', views.signupint, name='signupint'),
	url(r'^signupform/', views.signupform, name='signupform'),
	url(r'^signupexpert/', views.signupexpert, name='signupexpert'),
	url(r'^contactus/', views.contactus, name='contactus'),
	
]