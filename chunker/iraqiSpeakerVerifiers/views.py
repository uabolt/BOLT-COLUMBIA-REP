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
from django.http import HttpResponseRedirect


class SpeakerVerificationCreate(CreateView):
    model = SpeakerVerification
    fields = ['amt_id', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7']

    def get(self, request):
        ''' GET handler - here we check if the same user, identified by its session id,
            has already taken the test and direct him appropriately '''

        key = request.session.session_key

        qs = SpeakerVerification.objects.filter(session_key = key)

        # If there is no record in the queryset, display the form
        if qs.count() == 0:
            return super(SpeakerVerificationCreate, self).get(request)
        # If there is one record
        elif qs.count() == 1:
            record = qs[0]

            if record.is_passing:
                test_result = test_passed
            else:
                test_result = test_failed
        else:
            assert(False, "There shouln't be more than a single test for a given user")

        return HttpResponseRedirect(reverse(test_result))

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

        # Store which browser took this test
        form.instance.session_key = self.request.session.session_key

        super(SpeakerVerificationCreate, self).form_valid(form)

        if form.is_valid():
            return HttpResponseRedirect(reverse(test_result))
        else:
            return HttpResponseRedirect(reverse(test_failed))


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
