''' This file contains the code that exports the contents of the database into a TSV file
    which will fed the pipeline for the modeling '''


from django.core.management.base import BaseCommand, CommandError
from interface.models import *
from catalogs.utils import *


class Command(BaseCommand):
    ''' This is the class that implements the command for Django '''

    help = 'This exports the POS annotations into a TSV file\
 which will fed the pipeline for the modeling'

    def handle(self, *args, **options):
        ''' Implementation of the command '''

        # Get all the survey codes
        codes = [i for i in POSAnnotation.objects.values_list('user_code', flat=True).distinct() if i]

        for code in codes:

            pos = POSAnnotation.objects.filter(user_code= code).order_by('ref_id')
            reph = RephAnnotation.objects.filter(user_code= code).order_by('ref_id')

            if pos_seems_legit(pos):
                # Only if the annotations look legit

                for p in pos:
                    # Make them TSV
                    # Format:
                    # ref_id sentence error_span legible (0:No,1:Yes,2:Unknown) error_guess targeted_question continue_process (1:True,0:False) POS_list
                    values = [p.ref_id, p.reference]

                    # Compute the index of the error segment
                    words = p.masked.split()

                    start = stop = None

                    for i, w in enumerate(words):
                        if '_' in w: # A masked word
                            if start == None:
                                start = i
                            stop = i

                    values.append('%i-%i' % (start, stop))

                    values.extend([str(p.legible), p.guess, p.question, str(int(p.continue_process))])

                    # Fetch the POS tags
                    tags = ','.join([t.POS for t in p.postag_set.all()])

                    values.append(tags)

                    out = '\t'.join(values)

                    # Print the result
                    self.stdout.write(out)
