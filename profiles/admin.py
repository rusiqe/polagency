from django.contrib import admin
from .models import Profile, Milestone, ProfileMilestone

admin.site.register(Profile)
admin.site.register(Milestone)
admin.site.register(ProfileMilestone)
