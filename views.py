from django.shortcuts import render
# Create your views here.
from django.template import loader
from .models import Link, Datapoint, Expert, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from .forms import *
from datetime import datetime

#addlink functionality must be restricted for users, can be done by adding context, checking with js

def login(request):
	if request.method=='POST':
		form = ValidationForm(request.POST)
		print(form.is_valid())
		print(form)
		#reeplace 404s with error messages later
		
		if(form.is_valid()):
			uname = form.cleaned_data['username']
			pword = form.cleaned_data['password']
			con=True
			try:
				User.objects.get(username=uname)
			except User.DoesNotExist:
				con=False
			con2 = True
			try:
				Expert.objects.get(username=uname)
			except Expert.DoesNotExist:
				con2=False
			if con:
				print(User.objects.get(username=uname))
				pw = True
				try:
					if(not pword == User.objects.get(username=uname).password):
						return render(request, 'linkpedia/login_page.html', {'validationfailure':'Password or username does not exist.'})
				except User.DoesNotExist:
					pw=False
				if pw:
					pword == User.objects.get(username=uname).password
					return redirect('http://127.0.0.1:8000/linkpedia/home/user/'+uname)
				else:
					print('a')
					return render(request, 'linkpedia/login_page.html', {'validationfailure':'Password or username does not exist.'})
			elif con2:
				pw = True
				try:
					if(not pword == Expert.objects.get(username=uname).password):
						return render(request, 'linkpedia/login_page.html', {'validationfailure':'Password or username does not exist.'})
				except Expert.DoesNotExist:
					pw=False
				if pw:
					pword == Expert.objects.get(username=uname).password
					return redirect('http://127.0.0.1:8000/linkpedia/home/expert/'+uname)
				else:
					print('b')
					return render(request, 'linkpedia/login_page.html', {'validationfailure':'Password or username does not exist.'})
			else:
				print('c')
				return render(request, 'linkpedia/login_page.html', {'validationfailure':'Password or username does not exist.'})
		else:
			return render(request, 'linkpedia/login_page.html', {'validationfailure':'Password or username does not exist.'})
	else:
		form = ExpertForm(initial={})
		return render(request, 'linkpedia/login_page.html', {})

def home(request, username):
	u=True
	e = True
	try:
		print(User.objects.get(username=username))
	except User.DoesNotExist:
		u=False
	try:
		Expert.objects.get(username=username)
	except Expert.DoesNotExist:
		e=False
	if u:
		return render(request,'linkpedia/home_page.html', {'user':User.objects.get(username=username), 'exists':'','datapoints':(Datapoint.objects.all()),'links':(Link.objects.all())})
	else:
		return render(request,'linkpedia/home_page.html', {'user':Expert.objects.get(username=username), 'exists':('Add Link'),'datapoints':(Datapoint.objects.all()),'links':(Link.objects.all())})
	
def viewprofile(request, username):
	u=True
	try:
		print(User.objects.get(username=username))
	except User.DoesNotExist:
		u=False
	e = True
	try:
		Expert.objects.get(username=username)
	except Expert.DoesNotExist:
		e=False
	if u:
		return render(request,'linkpedia/profile_page.html', {'user':User.objects.get(username=username)})
	else:
		return render(request,'linkpedia/profile_page.html', {'user':Expert.objects.get(username=username)})

def addcontent(request, username):
	u=True
	try:
		print(User.objects.get(username=username))
	except User.DoesNotExist:
		u=False
	e = True
	try:
		Expert.objects.get(username=username)
	except Expert.DoesNotExist:
		e=False
		
	if request.method=='POST':
		form = ContentForm(request.POST)
		if form.is_valid():
			Datapoint.objects.create(timestamp=datetime.now(),country=form.cleaned_data['country'],data_url=form.cleaned_data['data_url'],data_title=form.cleaned_data['data_title'],data_description=form.cleaned_data['data_description'])
			print('here')
			if(u):
				return redirect('http://127.0.0.1:8000/linkpedia/home/user/'+username)
			else:
				return redirect('http://127.0.0.1:8000/linkpedia/home/expert/'+username)
		else:
			raise Http404
	else:
		form = ContentForm(initial={})
		return render(request,'linkpedia/add_content_page.html',{})
	
def addlink(request, username):
	if request.method=='POST':
		form = LinkForm(request.POST)
		if form.is_valid():
			Link.objects.create(content_one_url=form.cleaned_data['content_one_url'],content_two_url=form.cleaned_data['content_two_url'],link_title=form.cleaned_data['link_title'],link_description=form.cleaned_data['link_description'],timestamp=datetime.now(),link_rating=3.0)
			return redirect('http://127.0.0.1:8000/linkpedia/home/expert/'+username)
		else:
			raise Http404
	else:
		form = LinkForm(initial={})
		return render(request,'linkpedia/add_link_page.html',{})
	
def linkinfo(request, id):
	link = get_object_or_404(Link, pk=id)
	if request.method=='POST':
		form = RatingForm(request.POST)
		print (form.is_valid());
		if form.is_valid():
			new = form.cleaned_data['link_rating']
			old = link.link_rating
			num = link.number_of_ratings
			average = (old*num+new)/(num+1)
			link.number_of_ratings +=1
			link.link_rating = average
			link.save()
			return render(request,'linkpedia/linkinfo_page.html',{'link':link})
		else:
			print('over here')
			raise Http404
	else:
		form = RatingForm(initial={})
		return render(request,'linkpedia/linkinfo_page.html',{'link':link})
	
	

def signupint(request):
	return render(request,'linkpedia/signupint_page.html',{})
	
def contactus(request):
	return render(request,'linkpedia/contactus_page.html',{})

def signupform(request):
	if request.method=='POST':
		form = UserForm(request.POST)
		print(form.is_valid())
		print(form)
		if form.is_valid():
			if form.cleaned_data['password']==form.cleaned_data['ogpword'] :
				User.objects.create(username=form.cleaned_data['username'],email=form.cleaned_data['email'],password=form.cleaned_data['password'])
				return redirect('http://127.0.0.1:8000/linkpedia/login/')
			else:
				return render(request,'linkpedia/signupform_page.html',{'donotmatch':"Passwords do not match. Please try again."})
		else:
			raise Http404
	else:
		form = UserForm(initial={})
		return render(request,'linkpedia/signupform_page.html',{})
def signupexpert(request):
	if request.method=='POST':
		form = ExpertForm(request.POST)
		print(form.is_valid())
		print(form)
		if form.is_valid():
			if form.cleaned_data['password']==form.cleaned_data['ogpword'] :
				Expert.objects.create(description_of_expertise=form.cleaned_data['description_of_expertise'],profession=form.cleaned_data['profession'],research_institution=form.cleaned_data['research_institution'],name=form.cleaned_data['name'],username=form.cleaned_data['username'],email=form.cleaned_data['email'],password=form.cleaned_data['password'])
				return redirect('http://127.0.0.1:8000/linkpedia/login/')
			else:
				return render(request,'linkpedia/signupexpert_page.html',{'donotmatch':"Passwords do not match. Please try again."})
		else:
			raise Http404
	else:
		form = ExpertForm(initial={})
		return render(request,'linkpedia/signupexpert_page.html',{})