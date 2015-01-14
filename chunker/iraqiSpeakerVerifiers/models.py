# -*- coding: utf-8 -*- 
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import uuid

class SpeakerVerification(models.Model):
    user_code = models.CharField(max_length=32, default=lambda:uuid.uuid4().hex)

    answer1 = models.CharField(max_length=200, verbose_name = _('Baghdad is divided into two major halves. What are they?'))

    answer2 = models.CharField(verbose_name = _("what are the common nicknames for the following Iraqi Names (Nickname starts with Abu): Ali,Hussein and Mohammed?"), max_length=200)

    answer3 = models.CharField(verbose_name = _("What's the two favorite games in almost all Iraqi coffee shops?"), max_length=200)

    answer4 = models.CharField(verbose_name = _("What's the meaning of the word \"Hashash\" in Iraqi slang?"), max_length=200)

    answer5 = models.CharField(verbose_name = _("What's the most popular type of bread in Iraq?"), max_length=200)

    answer6 = models.CharField(verbose_name = _("What's the most popular sport in Iraq?"), max_length=200)

    def get_absolute_url(self):
        return reverse('verification')

