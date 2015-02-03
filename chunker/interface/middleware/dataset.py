from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from os.path import basename, splitext
from interface.models import DatasetAssignment as DSA
from interface.models import *
import glob, random, os, shutil, re, pdb, chunker

pattern = re.compile(r'^/admin/?')

class AssignDataset:

    def process_request(self, request):
        ''' Assigns a dataset to the session if it doesn't exist yet. This middleware should go after the session middleware'''

        #if not pattern.match(request.path) and not reverse('finish') in request.path and not reverse('instructions') in request.path:
        if reverse('pos_annotation') in request.path or reverse('reph_annotation') in request.path:
            path = settings.DATASET_DIR

            # Dataset should be a non empty sequence on the
            if not 'dataset' in request.session or len(request.session['dataset']) == 0:

                # Retrieve the dataset files
                files = glob.glob(os.path.join(path, "*.ds"))

                if len(files) == 0:
                    return HttpResponseRedirect(reverse('finish'))

                l = 1
                while l != 0:
                    # Generate a random index
                    ix = random.randint(0, len(files)-1)

                    # Here we check if this dataset has been previously assigned to the same session_id
                    dsname = basename(files[ix]).split('.')[0]
                    qs = DSA.objects.filter(session_id = request.session.session_key).filter(file_prefix__startswith = dsname[:-2])

                    l = len(qs)

                obj = DSA(session_id = request.session.session_key, file_prefix= dsname)
                obj.save()



                # Read the contents
                with open(files[ix], 'r') as f:
                    fields = ('id', 'ref', 'chunked', 'segmented', 'control')
                    sentences = []
                    # Each line has format "id \t ref \t chunked \t segmented \t control(boolean field)
                    for line in f:
                        sentences.append(dict(zip(fields, line.split('\t'))))
                request.session['dataset'] = sentences
                request.session['ds_file'] = files[ix].split('/')[-1] # Last token, which is the actual file name

                # Move the file to the processed files folder
                path = os.path.join(path, 'processed')
                if not os.path.exists(path):
                    os.makedirs(path)

                shutil.move(files[ix], path)


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

    # import pdb
    # pdb.set_trace()
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

    return chunker.settings.TASK_SIZE - AnnotationRecord.objects.filter(annotator = user_id).count()

class DatasetExhaustedException(Exception):
    ''' Exception raised if the dataset has been exhausted

        The exhaustion is defined when all the elements have been annotated the number
        of times defined in chunker.settings.MAX_ANNOTATIONS or when the remaining elements
        are not suitable to be annotated by the current user

    '''
    pass
