# -*- coding: utf-8 -*-

# View for Iraqi Arabic fluency test form.
#
# Author: David Sidi <bolt_IA_validation_middleware.spamhungry@mamber.net>
#

"""
View for Iraqi Arabic fluency test form.

"""

from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin
from django.template import RequestContext

from iraqiSpeakerVerifiers.models import SpeakerVerification
from iraqiSpeakerVerifiers.models import ConsentVerification

from django.shortcuts import render


class SpeakerVerificationCreate(CreateView):
    model = SpeakerVerification
    fields = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7']

    def form_valid(self, form):
        """
        Have valid input, now check whether answers are right.

        If the submission succeeds, we take the user to a page with a token
        to give to AMTurk, and with a link to the rephrase experiment.
        """
        if is_correct_answer(form):
            form.instance.is_passing = True
            test_result = test_passed

        else:
            form.instance.is_passing = False  # for clarity. Default is False
            test_result = test_failed


        # set a flag so we know when a new task is initiated in this session
        self.request.session['finish_screen_seen'] = False

        ModelFormMixin.success_url = reverse(test_result)

        return super(SpeakerVerificationCreate, self).form_valid(form)


class SpeakerVerificationUpdate(UpdateView):
    model = SpeakerVerification
    fields = ['text']


def is_correct_answer(form):
    """
    Check the submitted answers for the presence of all of a set of checkwords.

    :return: True if the proportion correct is greater than 0.85
    :rtype: bool
    """
    given_answers = (
        form.instance.answer1, form.instance.answer2, form.instance.answer3,
        form.instance.answer4, form.instance.answer5, form.instance.answer6,
        form.instance.answer7
    )

    # in ascending order, with number 5 missing
    correct_answers_checkwords = (
        [u'الكرخ', u'الرصافة'],
        [u'أبو حسين', u'أبو علي', u'أبو جاسم'],
        [u'الدومنة', u'الطاولي'],
        [u'العيون'],
        # [u'العيون', 'عوجة'],
        [u'صمون', u'حجري'],
        [u'كرة', u'القدم'],
        [u'عوجة']
    )

    assert(len(correct_answers_checkwords) == len(given_answers))

    # Count correct answers.
    num_correct = 0
    for given_answer, correct_answer_checkwords in \
            zip(given_answers, correct_answers_checkwords):

        #  An answer is right if it has all the checkwords in it
        if all(map(lambda checkword: checkword in given_answer,
                   correct_answer_checkwords)):

            num_correct += 1

    return num_correct / (len(given_answers) * 1.) > 0.50

class ConsentVerificationCreate(CreateView):
    model = ConsentVerification
    fields = ['age_check', 'data_use_check']

    def form_valid(self, form):
        # pass user_code in the session, so that rephrase experiment can use it
        self.request.session['user_code'] = form.instance.user_code

        return super(ConsentVerificationCreate, self).form_valid(form)



def test_passed(request):
    context = RequestContext(request)
    return render(request, 'iraqiSpeakerVerifiers/testPassed.html', context)


def test_failed(request):
    context = RequestContext(request)
    return render(request, 'iraqiSpeakerVerifiers/testFailed.html', context)
