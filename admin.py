from django.contrib import admin

# Register your models here.
from .models import Datapoint, Link, Expert, User
admin.site.register(Datapoint)
admin.site.register(Link)
admin.site.register(Expert)
admin.site.register(User)
