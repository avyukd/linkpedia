# Create your models here.
from django.db import models
from copy import copy
# base class for Experts
from django.forms.widgets import *
from django import forms

class Expert(models.Model):
    # real full name
    # NOTE widget=forms.TextInput - how to change form to normal text input not text area- affects admin
    name = models.TextField(max_length=200)
    # username for logins
    username = models.CharField(max_length=200, unique=True)
    # pword for login
    password = models.TextField(max_length=200)
    # should be .edu or institution checked
    email = models.TextField(max_length=200)
    # based on link ratings and content quality
    expert_rating = models.DecimalField(decimal_places=1, max_digits=2, default=2.0)
    number_of_ratings = models.IntegerField(default=0)
    # idk may be helpful later
    timestamp = models.DateTimeField()
    def __str__(self):
        return self.username
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.username == other.username
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
# one to many with experts
class Profession(models.Model):
    # "Doctor" or something general
    title = models.CharField(max_length=200)
    # more specific explanation of job
    description_of_expertise = models.TextField(max_length=10000)
    # related institution to work or INDEPENDENT
    research_institution = models.TextField(max_length=200, default="INDEPENDENT")
    # just awards separated by commas
    specific_achievements = models.TextField(max_length=10000)
    # auto generated field bassed on above stuff plus thesauraus api + profession --> content api
    tags = models.TextField(max_length=10000)
    # idk may be helpful later
    timestamp = models.DateTimeField()
    # experts can have many professions
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    '''
    1.1- deleting bug
    FIX LATER:
    When deleting, models.CASCADE deletes the original expert entry as well- not what is wanted- 
    find way to make on_delete so that it only deletes the profession rather than the expert too
    possible options:
        - SET() after copying the original expert using signals and receivers
        - don't delete just set instance of profession to null and don't iterate over it?
        - store temporary copy of entire structure and rebuild it after the delete
    '''
#module to suggest experts to join Linkpedia- recommendations basically or vetting system
class Suggestion(models.Model):
    # name of expert being recommended
    name = models.TextField(max_length=200)
    # email of said expert
    email = models.TextField(max_length=200)
    # idk may be helpful later
    timestamp = models.DateTimeField()
    # auto generated info for initial login
    auto_uname = models.CharField(max_length=15,unique=True)
    auto_pword = models.TextField(max_length=15)
    # experts can have many suggestions
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    # 1.1 applies
    '''
    NOTE: 
    For this module to fully work, features must be implemented to update information profile related first
    '''

'''
Additional Setup:
- Background check hueristic
- Achievements cross checker
- Linkedln Name API
'''

# base class link
class Link(models.Model):
    # accessing both datapoints being linked
    content_one_pk = models.IntegerField()
    content_two_pk = models.IntegerField()
    # use two contents plus relationship phrase for best
    title = models.CharField(max_length=200,unique=True)
    # general description
    description = models.TextField(max_length=10000)
    # useful for later
    timestamp = models.DateTimeField()
    # rating of link
    link_rating = models.DecimalField(decimal_places=1, max_digits=2)
    number_of_ratings = models.IntegerField(default=0)
    # expert who creates the link or new version of the link
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    # version number to keep track of indices
    version = models.IntegerField(default=1)
    #coords for lines between datapoints
    lat1, long1, lat2, long2 = \
        models.DecimalField(decimal_places=2, max_digits=5, default=0.0),\
        models.DecimalField(decimal_places=2, max_digits=5, default=0.0),\
        models.DecimalField(decimal_places=2, max_digits=5, default=0.0),\
        models.DecimalField(decimal_places=2, max_digits=5, default=0.0)

    def __str__(self):
        return self.title

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.title == other.title
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Datapoint(models.Model):
    url = models.CharField(max_length=200, unique=True)
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=10000)
    timestamp = models.DateTimeField()
    # later update this with a navigable map on the front end
    version = models.IntegerField(default=1)
    content_rating = models.DecimalField(decimal_places=1, max_digits=2)
    number_of_ratings = models.IntegerField(default=0)
    # separate by commas auto generate
    tags = models.TextField(max_length=10000)
    linked = models.BooleanField(default=False)
    # should be one of three things: an expert username, user username, or AUTO
    creator = models.TextField(max_length=200)
    def __str__(self):
        return self.url


class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField(max_length=200)
    email = models.TextField(max_length=200)
    timestamp = models.DateTimeField()
    def __str__(self):
        return self.username
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.username == other.username
        return False
    def __ne__(self, other):
        return not self.__eq__(other)