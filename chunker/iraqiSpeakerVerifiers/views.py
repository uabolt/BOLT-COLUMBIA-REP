# -*- coding: utf-8 -*-

# View for Iraqi Arabic fluency test form.
#
# Author: David Sidi <bolt_IA_validation_middleware.spamhungry@mamber.net>
#

"""
View for Iraqi Arabic fluency test form.

"""


from django.conf import settings
from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin
from django.template import RequestContext

from iraqiSpeakerVerifiers.forms import validationForm
from iraqiSpeakerVerifiers.models import SpeakerVerification

from django.shortcuts import render 
from django.http import HttpResponseRedirect




class SpeakerVerificationCreate(CreateView):
    model = SpeakerVerification
    fields = ['answer1', 'answer2', 'answer3','answer4','answer5','answer6', 'answer7']


    def form_valid(self, form):
        ''' 
        Have valid input, now check whether answers are right.

        If the submission succeeds, we take the user to a page with a token
        to give to AMTurk, and with a link to the rephrase experiment.
        '''
        if is_correct_answer(form):
            form.instance.is_passing = True
            test_result = test_passed
                    
        else:
            form.instance.is_passing = False # for clarity. Default is False
            test_result = test_failed

        ModelFormMixin.success_url = reverse(test_result,
                kwargs={'user_code':form.instance.user_code})

        return super(SpeakerVerificationCreate, self).form_valid(form)


class SpeakerVerificationUpdate(UpdateView):
    model = SpeakerVerification
    fields = ['text']


def is_correct_answer(form):
    '''
    Check the submitted answers for the presence of all of a set of checkwords.

    :return: True if the proportion correct is greater than 0.85
    :rtype: bool
    '''
    # NOTE: answer5 ommitted
    given_answers = \
        form.instance.answer1, form.instance.answer2, form.instance.answer3, \
        form.instance.answer4, form.instance.answer6


    # in ascending order, with number 5 missing
    #TODO fix replaced hashash q with "see nothing but food." added q7
    correct_answers_checkwords = ( \
        [u'الكرخ', u'الرصافة'], \
        [u'أبو حسين', u'أبو علي', u'أبو جاسم'], \
        [u'الدومنة', u'الطاولي'], \
        [u'العيون', u'عوجة'], \
        [u'صمون', u'حجري'], \
        [u'كرة', u'القدم'] \
    )


    # Count correct answers.
    numCorrect = 0
    for given_answer, correct_answer_checkwords in \
            zip(given_answers, correct_answers_checkwords):

        #  An answer is right if it has all the checkwords in it
        if all(map(lambda checkword: checkword in given_answer, 
                correct_answer_checkwords)):

            numCorrect += 1

    return numCorrect / (len(given_answers) * 1.) > 0.85


def test_passed(request, user_code):
    context = RequestContext(request, {
        'user_code': user_code,
        })

    return render(request, 'iraqiSpeakerVerifiers/testPassed.html', context)


def test_failed(request, user_code):
    context = RequestContext(request, {
        'user_code': user_code,
        })

    return render(request, 'iraqiSpeakerVerifiers/testFailed.html', context)

