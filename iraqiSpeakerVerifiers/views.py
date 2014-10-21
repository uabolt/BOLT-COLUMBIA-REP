# -*- coding: utf-8 -*-
from iraqiSpeakerVerifiers.forms import validationForm
from django.views.generic.edit import CreateView, UpdateView
from iraqiSpeakerVerifiers.models import SpeakerVerification

class SpeakerVerificationCreate(CreateView):
    model = SpeakerVerification
    fields = ['answer1', 'answer2', 'answer3','answer4','answer5','answer6']

class SpeakerVerificationUpdate(UpdateView):
    model = SpeakerVerification
    fields = ['text']

