from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Event)
admin.site.register(models.TripInviteRequest)
admin.site.register(models.TripAttendees)
admin.site.register(models.Question)
admin.site.register(models.Choice)