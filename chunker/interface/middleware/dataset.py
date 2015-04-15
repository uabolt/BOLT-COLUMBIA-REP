from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from os.path import basename, splitext
from interface.models import DatasetAssignment as DSA
from interface.models import *
from iraqiSpeakerVerifiers.models import *
import glob, random, os, shutil, re, pdb, chunker

pattern = re.compile(r'^/admin/?')

class VerifyTestTaken:

    def process_request(self, request):

        if reverse('pos_annotation') in request.path or reverse('reph_annotation') in request.path or reverse('sri-pos_annotation') in request.path:

            if reverse('sri-pos_annotation') in request.path:
                sri = True
            else:
                sri = False

            key = request.session.session_key

            qs = MultipleChoiceVerification.objects.filter(session_key = key)

            # If there is no record in the queryset, display the form
            if qs.count() == 0:
                if sri:
                    return HttpResponseRedirect(reverse('sri-root'))
                else:
                    return HttpResponseRedirect(reverse('root'))
            # If there is one record
            elif qs.count() == 1:
                record = qs[0]

                if record.is_passing:
                    return None
                else:
                    if sri:
                        return HttpResponseRedirect(reverse('sri-root'))
                    else:
                        return HttpResponseRedirect(reverse('root'))
            else:
                raise  Exception("There shouln't be more than a single test for a given user")


class AssignDataset:

    def process_request(self, request):
        ''' Assigns a dataset to the session if it doesn't exist yet. This middleware should go after the session middleware'''

        if reverse('pos_annotation') in request.path or reverse('reph_annotation') in request.path or reverse('sri-pos_annotation') in request.path:

            # Check wether we are done with all annotations to show the landing page
            if AnnotationRecord.objects.filter(annotator = request.session.session_key).count() == DataItem.objects.count():
                return HttpResponseRedirect(reverse('landing'))

            # Time for a new sentence!
            if not 'item' in request.session:
                # Get the "user_id"
                user_id = request.session.session_key

                # Is the task complete?
                if remaining_sentences_in_task(user_id) == chunker.settings.TASK_SIZE:


                    if not 'finish_screen_seen' in request.session:
                        if reverse('sri-pos_annotation') in request.path:
                            return HttpResponseRedirect(reverse('sri-finish'))
                        else:
                            return HttpResponseRedirect(reverse('finish'))

                try:
                    item = assign_sentence(user_id)
                    request.session['item'] = item.id

                    # Necessary to don't get stuck in the finish screen
                    if 'finish_screen_seen' in request.session:
                        del request.session['finish_screen_seen']

                except DatasetExhaustedException as e:
                    return HttpResponseRedirect(reverse('finish'))

        return None


# Assignment functions
def assign_sentence(user_id):
    '''
        Gets a user_id, which is its session key, and returns an instance of DataItem

        The dataset item shouldn't have been seen by the same user before and it
        should be comprenhensive, meaning that before showing the same dataset item
        to another user, all the elements of the dataset should be annotated by someone
        for the current round, unless the remaining elements have already been seen by the
        current user.
    '''

    # Get the items orderdered by number of annotations and by sequence number (pk)
    items = DataItem.objects.annotate(num_annotations = Count('annotationrecord')).exclude(num_annotations__gte = chunker.settings.MAX_ANNOTATIONS).order_by('num_annotations').order_by('pk')

    # First, return the first DataItem with no annotations
    non_annotated = items.filter(num_annotations = 0)

    if non_annotated.count() > 0:
        ret = non_annotated[0]
    else:
        # Now, get the first item not annotated by the current user
        items = items.exclude(annotationrecord__annotator = user_id)

        if items.count() == 0:
            raise DatasetExhaustedException()
        else:
            ret = items[0]

    r = AnnotationRecord()
    r.item = ret
    r.annotator = user_id
    r.save()

    return ret

def remaining_sentences_in_task(user_id):
    '''
        Returns the number of remaining elements needed to complete a task.

        Its value should be within 0 and chunker.settings.TASK_SIZE
    '''

    return chunker.settings.TASK_SIZE - (AnnotationRecord.objects.filter(annotator = user_id).count() % chunker.settings.TASK_SIZE)

class DatasetExhaustedException(Exception):
    ''' Exception raised if the dataset has been exhausted

        The exhaustion is defined when all the elements have been annotated the number
        of times defined in chunker.settings.MAX_ANNOTATIONS or when the remaining elements
        are not suitable to be annotated by the current user

    '''
    pass
