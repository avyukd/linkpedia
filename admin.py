from django.contrib import admin
# Register your models here.
from .models import Datapoint, Profession, Suggestion, Link, Expert, User
admin.site.register(Datapoint)
admin.site.register(Link)
admin.site.register(Expert)
admin.site.register(User)
admin.site.register(Suggestion)
admin.site.register(Profession)