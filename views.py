from __future__ import print_function

from django.shortcuts import render
# Create your views here.
from django.template import loader
from .models import Link, Datapoint, Expert, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from .forms import *

from datetime import datetime
import html2text
import requests
from collections import Counter
from string import punctuation
import re
import random
from six.moves.urllib import request
import geojson
import json
from google import search

# addlink functionality must be restricted for users, can be done by adding context, checking with js
# get plain text

def cross_check(query):
    score = 0
    for url in search(query, tld='com', lang='es', stop=5):
        source_code = requests.get(url)
        html = source_code.text
        m = (html2text.html2text(html))
        if query.split("AND")[0] in m:
            score+=1
    return score/5
def gen_tags(string, lim):
    lst = list(str(string))
    lst = [x.lower() for x in lst]
    counter = Counter(lst)
    occs = [(word, count) for word, count in counter.items() if count > lim]
    occs.sort(key=lambda x: x[1])
    print(occs)
    fr = open("commonwords", "r")
    li = fr.read().split("\n")
    final = []
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for a in occs:
        if a[0] not in li:
            con = True
            for nex in a[0]:
                if nex in nums:
                    con = False
            if con:
                if len(a[0]) > 1:
                    final.append(a)
    if len(final)==0:
        return ''
    return ','.join(final)
def suggestion_score(tgs, desc_of_exp, profession, research_institution):
    score = 0
    words = desc_of_exp.split(" ") + profession.split(" ") + profession.split(" ")
    for t in tgs.split(" "):
        for w in words:
            if w in t:
                score += 1
    return score


def mapjs(request):
    return render(request, 'linkpedia/result.js', {})


def retTags(url):
    source_code = requests.get(url)
    html = source_code.text
    m = (html2text.html2text(html))
    lst = re.findall(r'\b\w+', m)
    lst = [x.lower() for x in lst]
    counter = Counter(lst)
    occs = [(word, count) for word, count in counter.items() if count > 5]
    occs.sort(key=lambda x: x[1])
    print(occs)
    fr = open(r"C:\Users\Avyuk Dixit\linkpediav1\linkpedia\common.txt", "r")
    list = fr.read().split("\n")
    final = []
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for a in occs:
        if a[0] not in list:
            con = True
            for nex in a[0]:
                if nex in nums:
                    con = False
            if con:
                if len(a[0]) > 1:
                    final.append(a)
    t = []
    for v, f in final:
        t.append(v)
    return " ".join(t)

def login(request):
    if request.method == 'POST':
        form = ValidationForm(request.POST)
        '''NOTE
        replace 404s with error messages later'''
        if form.is_valid():
            uname = form.cleaned_data['username']
            pword = form.cleaned_data['password']
            con = True
            try:
                User.objects.get(username=uname)
            except User.DoesNotExist:
                con = False
            con2 = True
            try:
                Expert.objects.get(username=uname)
            except Expert.DoesNotExist:
                con2 = False
            if con:
                pw = True
                try:
                    if (not pword == User.objects.get(username=uname).password):
                        return render(request, 'linkpedia/login_page.html',
                                      {'validationfailure': 'Password or username does not exist.'})
                except User.DoesNotExist:
                    pw = False
                if pw:
                    return redirect('http://127.0.0.1:8000/linkpedia/home/user/' + uname)
                else:
                    print('a')
                    return render(request, 'linkpedia/login_page.html',
                                  {'validationfailure': 'Password or username does not exist.'})
            elif con2:
                pw = True
                try:
                    if (not pword == Expert.objects.get(username=uname).password):
                        return render(request, 'linkpedia/login_page.html',
                                      {'validationfailure': 'Password or username does not exist.'})
                except Expert.DoesNotExist:
                    pw = False
                if pw:
                    return redirect('http://127.0.0.1:8000/linkpedia/home/expert/' + uname)
                else:
                 return render(request, 'linkpedia/login_page.html',
                                  {'validationfailure': 'Password or username does not exist.'})
            else:
                return render(request, 'linkpedia/login_page.html',
                              {'validationfailure': 'Password or username does not exist.'})
        else:
            return render(request, 'linkpedia/login_page.html',
                          {'validationfailure': 'Password or username does not exist.'})
    else:
        form = ExpertForm(initial={})
        return render(request, 'linkpedia/login_page.html', {})

def home(request, username):
    u = True
    e = True
    try:
        print(User.objects.get(username=username))
    except User.DoesNotExist:
        u = False
    try:
        Expert.objects.get(username=username)
    except Expert.DoesNotExist:
        e = False
    # change later- this is temporary and only works for small amounts of datapoints
    # add expert functionality to users later
    # image maps????
    if u:
        return render(request, 'linkpedia/home_page.html', {'user': User.objects.get(username=username), 'exists': '',
                                                            'datapoints': (Datapoint.objects.all()),
                                                            'links': (Link.objects.all())})
    else:

        # untagged stuff
        l = []
        e = Expert.objects.get(username=username)
        for d in Datapoint.objects.filter(linked=False):
            l.append((suggestion_score(d.tags, e.description_of_expertise, e.profession,
                                       e.research_institution) + random.uniform(0, 1), d))
        print((sorted(l)[::-1]))
        if len(l) > 100:
            l = [n[1] for n in sorted(l)[::-1][0:100]]
        else:
            l = [n[1] for n in sorted(l)[::-1]]
        # links for map
        maplinks = []
        for li in Link.objects.all():
            maplinks.append((suggestion_score((Datapoint.objects.filter(data_url=li.content_one_url)[0].tags +
                                               Datapoint.objects.filter(data_url=li.content_two_url)[0].tags),
                                              e.description_of_expertise, e.profession,
                                              e.research_institution) + random.uniform(0, 1), li))
        print((sorted(maplinks)[::-1]))
        if len(maplinks) > 100:
            maplinks = [n[1] for n in sorted(maplinks)[::-1][0:100]]
        else:
            maplinks = [n[1] for n in sorted(maplinks)[::-1]]
        final_links = []
        for nextlink in maplinks:
            d1 = Datapoint.objects.filter(data_url=nextlink.content_one_url)[0]
            final_links.append({"lat": int(d1.latitude), "lng": int(d1.longitude)})
            d2 = Datapoint.objects.filter(data_url=nextlink.content_two_url)[0]
            final_links.append({"lat": int(d2.latitude), "lng": int(d1.longitude)})

        output = "myFunction(" + json.dumps(final_links) + ");"
        fw = open(r'C:\Users\Avyuk Dixit\linkpediav1\linkpedia\templates\linkpedia\result.js', 'w')
        fw.write(output)
        fw.close()
        return render(request, 'linkpedia/home_page.html',
                      {'user': Expert.objects.get(username=username), 'exists': ('Add Link'), 'datapoints': (l),
                       'links': (Link.objects.all())})


def viewprofile(request, username):
    u = True
    try:
        print(User.objects.get(username=username))
    except User.DoesNotExist:
        u = False
    e = True
    try:
        Expert.objects.get(username=username)
    except Expert.DoesNotExist:
        e = False
    if u:
        return render(request, 'linkpedia/profile_page.html', {'user': User.objects.get(username=username)})
    else:
        return render(request, 'linkpedia/profile_page.html', {'user': Expert.objects.get(username=username)})


def addcontent(request, username):
    u = True
    try:
        print(User.objects.get(username=username))
    except User.DoesNotExist:
        u = False
    e = True
    try:
        Expert.objects.get(username=username)
    except Expert.DoesNotExist:
        e = False

    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            # retTags(form.cleaned_data['data_url'])
            Datapoint.objects.create(content_rating=3.0, tags=retTags(form.cleaned_data['data_url']),
                                     timestamp=datetime.now(), latitude=form.cleaned_data['latitude'],
                                     longitude=form.cleaned_data['longitude'], city=form.cleaned_data['city'],
                                     country=form.cleaned_data['country'], data_url=form.cleaned_data['data_url'],
                                     data_title=form.cleaned_data['data_title'],
                                     data_description=form.cleaned_data['data_description'])
            print('here')
            if u:
                return redirect('http://127.0.0.1:8000/linkpedia/home/user/' + username)
            else:
                return redirect('http://127.0.0.1:8000/linkpedia/home/expert/' + username)
        else:
            raise Http404
    else:
        form = ContentForm(initial={})
        return render(request, 'linkpedia/add_content_page.html', {})


def addlink(request, username):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        validlinks = [d.data_url for d in Datapoint.objects.all()]
        print(validlinks)
        print(form.is_valid())
        if form.is_valid():
            print((form.cleaned_data['content_one_url'] in validlinks) and (
            form.cleaned_data['content_two_url'] in validlinks))
            if (form.cleaned_data['content_one_url'] not in validlinks) and (
                form.cleaned_data['content_two_url'] not in validlinks):
                return render(request, 'linkpedia/add_link_page.html', {
                    'DNEerror': 'The link entered does not exist as a content in our database. Please add this url as content, find a different content.'})
            else:
                Link.objects.create(content_one_url=form.cleaned_data['content_one_url'],
                                    content_two_url=form.cleaned_data['content_two_url'],
                                    link_title=form.cleaned_data['link_title'],
                                    link_description=form.cleaned_data['link_description'], timestamp=datetime.now(),
                                    link_rating=3.0)
                a = Datapoint.objects.filter(data_url=form.cleaned_data['content_one_url'])[0]
                a.linked = True
                a.save()
                b = Datapoint.objects.filter(data_url=form.cleaned_data['content_two_url'])[0]
                b.linked = True
                b.save()
                return redirect('http://127.0.0.1:8000/linkpedia/home/expert/' + username)
        else:
            print("failure")
            raise Http404
    else:
        form = LinkForm(initial={})
        return render(request, 'linkpedia/add_link_page.html', {})


def linkinfo(request, id):
    link = get_object_or_404(Link, pk=id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            new = form.cleaned_data['link_rating']
            old = link.link_rating
            num = link.number_of_ratings
            average = (old * num + new) / (num + 1)
            link.number_of_ratings += 1
            link.link_rating = average
            link.save()
            return render(request, 'linkpedia/linkinfo_page.html', {'link': link})
        else:
            print('over here')
            raise Http404
    else:
        form = RatingForm(initial={})
        return render(request, 'linkpedia/linkinfo_page.html', {'link': link})


def signupint(request):
    return render(request, 'linkpedia/signupint_page.html', {})


def contactus(request, username):
    return render(request, 'linkpedia/contactus_page.html', {'ex': username})


def signupform(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['ogpword']:
                User.objects.create(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'], timestamp = datetime.now())
                return redirect('http://127.0.0.1:8000/linkpedia/login/')
            else:
                return render(request, 'linkpedia/signupform_page.html',
                              {'donotmatch': "Passwords do not match. Please try again."})
        else:
            raise Http404
    else:
        form = UserForm(initial={})
        return render(request, 'linkpedia/signupform_page.html', {})


def signupexpert(request):
    if request.method == 'POST':
        form = ExpertForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['ogpword']:
                uname = form.cleaned_data['username']
                Expert.objects.create(name=form.cleaned_data['name'], username=uname,
                                      email=form.cleaned_data['email'], password=form.cleaned_data['password'],
                                      timestamp=datetime.now())
                return redirect('http://127.0.0.1:8000/linkpedia/addprofession/'+uname)
            else:
                return render(request, 'linkpedia/signupexpert_page.html',
                              {'donotmatch': "Passwords do not match. Please try again."})
        else:
            raise Http404
    else:
        form = ExpertForm(initial={})
        return render(request, 'linkpedia/signupexpert_page.html', {})
# Create your views here.
def addprofession(request, username):
    e = Expert.objects.get(username=username)
    if request.method == 'POST':
        form = ProfessionForm(request.POST)
        if form.is_valid():
            print("a")
            t,doe,ri,sa = form.cleaned_data['title'],form.cleaned_data['description_of_expertise'],form.cleaned_data['research_institution'],form.cleaned_data['specific_achievements']
            print("b")
            Profession.objects.create(title=t, description_of_expertise=doe, specific_achievements=sa,research_institution=ri, timestamp=datetime.now(), expert=e,tags=gen_tags(sa+doe+ri+t,1))
            allachievements = str(sa).split(",")
            #add call to cross_check
            cum = 0
            for achieve in allachievements:
                cum += cross_check(e.name + " AND " + achieve)
            e.expert_rating = float(e.expert_rating) + cum/len(allachievements)
            e.save()
            return redirect('http://127.0.0.1:8000/linkpedia/login/')
        else:
            raise Http404
    else:
        form = ProfessionForm(initial={'RelatedExpert':e})
        return render(request, 'linkpedia/professionform.html',{})
        # Create your views here.