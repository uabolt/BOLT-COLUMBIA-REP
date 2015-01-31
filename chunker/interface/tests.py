from django.test import TestCase
import chunker
from interface.middleware.dataset import *
from interface.models import DataItem, AnnotationRecord

# Create your tests here.
class DataSetAssignmentTests(TestCase):
    fixtures = ['dataset_test']

    user1 = 'u1'
    user2 = 'u2'

    @classmethod
    def setUpClass(self):
        ''' Setup code for the test case '''

        # Set the maximum number of annotations to 2
        chunker.settings.MAX_ANNOTATIONS = 2
        chunker.settings.TASK_SIZE = 3 # This is for convenience as well

        # Populate some assignments
        self.i1 = DataItem.objects.get(ref_id='evalTranstac-0702-fieldStructured1-120')
        self.i2 = DataItem.objects.get(ref_id='evalTranstac-0702-fieldStructured1-128')
        self.i3 = DataItem.objects.get(ref_id='evalTranstac-0702-fieldStructured1-130')

        r1, r2 = AnnotationRecord(), AnnotationRecord()

        r1.item = self.i1
        r1.annotator = self.user1
        r2.item = self.i2
        r2.annotator = self.user2


        r1.save()
        r2.save()

    def test_task_size(self):
        ''' This tests the number of remaining sentences in a task '''

        num = AnnotationRecord.objects.filter(annotator = self.user1).count()

        self.assertEqual(remaining_sentences_in_task(self.user1), chunker.settings.TASK_SIZE - num) # Because in here the task size is 3

    def test_get_remaining_element(self):
        ''' This test checks that the comprenhensive feature is enforced '''

        item = assign_sentence(self.user1)

        self.assertEqual(item.id, 3)

    def test_number_of_records(self):
        ''' Checks if the AnnotationRecord instances is updated properly '''

        self.assertEqual(AnnotationRecord.objects.count(), 3)

    def test_respect_limits(self):
        ''' Checks that the system doesn't allow more annotations '''

        # Make some fake records
        for i in range(2):
            r = AnnotationRecord()
            r.item = self.i1
            r.annotator = self.user1
            r.save()

            r = AnnotationRecord()
            r.item = self.i2
            r.annotator = self.user1
            r.save()

            r = AnnotationRecord()
            r.item = self.i3
            r.annotator = self.user1
            r.save()

        # Now, there should be an exception
        self.assertRaises(DatasetExhaustedException, assign_sentence, self.user2)
