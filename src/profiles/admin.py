from django.contrib import admin
from .models import Profile, Relationship
# Register your models here.
# then you will see it at /admin/ route

admin.site.register(Profile)
admin.site.register(Relationship)