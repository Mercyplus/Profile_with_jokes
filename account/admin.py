from django.contrib import admin
from .models import Profile, Jokes


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Jokes)
