from django.db import models

# Used for registering users for a conference
class ConferenceRegistration(models.Model):
    # Required entries: name, email, sessions
    name =           models.CharField(max_length=250, blank=True)
    organization =   models.CharField(max_length=250, blank=True)
    email =          models.EmailField(max_length=250, blank=True)
    sessions =       models.MultipleChoiceField(choices=refs.conf_session_choices, blank=True)
    foodinfo =       models.CharField(max_length=250, blank=True)
    accommodations = models.CharField(max_length=250, blank=True)
