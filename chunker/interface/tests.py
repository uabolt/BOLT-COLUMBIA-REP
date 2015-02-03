from django.test import TestCase
import chunker
from interface.middleware.dataset import *
from interface.models import DataItem, AnnotationRecord

# Create your tests here.
class DataSetAssignmentTests(TestCase):
    fixtures = ['dataset_test.json']

    user1 = 'u1'
    user2 = 'u2'
    user3 = 'u3'
    user4 = 'u4'

    @classmethod
    def setUp(self):
        ''' Setup code for the test case '''

        # Set the maximum number of annotations to 2
        chunker.settings.MAX_ANNOTATIONS = 2
        chunker.settings.TASK_SIZE = 3 # This is for convenience as well

        # Populate some assignments
        self.i1 = DataItem.objects.get(pk=1)
        self.i2 = DataItem.objects.get(pk=2)
        self.i3 = DataItem.objects.get(pk=3)

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

        assign_sentence(self.user1)

        self.assertEqual(AnnotationRecord.objects.count(), 3)

    def test_exhaust_dataset(self):
        ''' Checks that the system doesn't allow a user to annotate any sentence more than once '''

        # Make some fake records
        assign_sentence(self.user2)
        assign_sentence(self.user2)

        # Now, there should be an exception
        self.assertRaises(DatasetExhaustedException, assign_sentence, self.user2)

        # But should allow another user to annotate something
        self.assertIsInstance(assign_sentence(self.user1), DataItem)

    def test_enforce_max_annotations(self):
        ''' Checks that MAX_ANNOTATIONS is enforced '''

        chunker.settings.MAX_ANNOTATIONS = 1

        assign_sentence(self.user3) # This annotates all sentences once

        # This should rise the exception because all sentences have been annotated
        # and the max number of annotations was 1
        self.assertRaises(DatasetExhaustedException, assign_sentence, self.user4)
