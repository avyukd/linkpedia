from django import forms
from .models import Expert, Datapoint, Link, User, Profession

'''
class ContentForm(forms.ModelForm):
    class Meta:
        model = Datapoint
        fields = ('data_url', 'data_title', 'data_description', 'latitude', 'longitude', 'country', 'city')


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('content_one_url', 'content_two_url', 'link_title', 'link_description')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('link_rating',)

'''
from linkpediav2.models import Expert, Profession


class ExpertForm(forms.ModelForm):
    ogpword = forms.CharField(max_length=500)

    class Meta:
        model = Expert
        fields = ('name', 'username', 'password', 'email')

class ProfessionForm(forms.ModelForm):
    class Meta:
        model = Profession
        fields = ('title','description_of_expertise','research_institution','specific_achievements')

class UserForm(forms.ModelForm):
    ogpword = forms.CharField(max_length=200)
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class ValidationForm(forms.Form):
    username = forms.CharField(max_length=1000)
    password = forms.CharField(max_length=1000)