from django.contrib import admin
from .models import Profile, Project, Review, Like, Follow

# Register your models here.

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(Follow)