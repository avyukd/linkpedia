from django.db import models


class Link(models.Model):
	
	content_one_url = models.CharField(max_length=200, unique = True)
	content_two_url = models.CharField(max_length=200, unique=True)
	link_title = models.CharField(max_length=500, unique=True)
	link_description = models.CharField(max_length=10000)
	timestamp = models.DateTimeField()
	link_rating  = models.DecimalField(decimal_places=1,max_digits=2)
	number_of_ratings = models.IntegerField(default=0)
	def __str__(self):
		return self.link_title
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.link_title == other.link_title
		return False
	def __ne__(self, other):
		return not self.__eq__(other)
		

class Datapoint(models.Model):
	data_url = models.CharField(max_length = 200, unique=True)
	data_title = models.CharField(max_length=50, unique=True)
	data_description = models.CharField(max_length=10000)
	timestamp = models.DateTimeField()
	country = models.CharField(max_length=50)
	def __str__(self):
		return self.data_url
		
class Expert(models.Model):
	name = models.CharField(max_length = 200)
	username = models.CharField(max_length = 200, unique=True)
	password = models.CharField(max_length = 200)
	profession = models.CharField(max_length = 200)
	research_institution = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	description_of_expertise = models.CharField(max_length = 1000)
	def __str__(self):
		return self.username
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.username == other.username
		return False
	def __ne__(self, other):
		return not self.__eq__(other)

class User(models.Model):
	username = models.CharField(max_length = 200, unique=True)
	password = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	def __str__(self):
		return self.username
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.username == other.username
		return False
	def __ne__(self, other):
		return not self.__eq__(other)