from django.db import models

# Create your models here.

class Annotation(models.Model):
    '''Class that represents an annotation for a sentence in IA'''

    POS_TAGS = (
        ('VRB', 'Verb'),
        ('NN', 'Noun'),
    )

    EASINESS_CHOICES = (
        (1, 'Strongly disagree'),
        (2, 'Disagree'),
        (3, 'More or less'),
        (4, 'Agree'),
        (5, 'Strongly agree'),
    )

    REPHRASE_CHOICES = (
        (0, 'Rephrase'),
        (1, 'Definition'),
    )

    # Control fields
    hypothesis = models.CharField(blank=False, max_length=255) # Ref without some chunks
    reference = models.CharField(blank=False, max_length=255) # The ref
    control_annotation = models.BooleanField(blank=False) # If this is true, then this annotation is used for control purposes
    date = models.DateField(auto_now_add=True)

    # Columbia experiment's fields
    legible = models.BooleanField(blank=False) # Is the sentence legible despite the missing chunks?
    guess = models.CharField(blank=True, max_length=50) # The guessed word, or blank if can't be guessed
    POS = models.CharField(blank=True, choices=POS_TAGS, max_length=7) # Part of speech tag of the guessed word
    question = models.CharField(blank=True, max_length=300) # Targeted question/definition to obtain the missing word

    # Rephrase fields
    eassines = models.IntegerField(default=3, choices=EASINESS_CHOICES) # How hard is it to rephrase
    local_rephrase = models.CharField(blank=True, max_length=75) # Local rephrase
    reph_type = models.IntegerField(blank=True, null=True, choices=REPHRASE_CHOICES) # What kind of answer is this
    local_merge = models.CharField(blank=True, max_length=255) # Local rephrase merged with the hyp
    global_rephrase = models.CharField(blank=True, max_length=255) # Rephrased sentences

    def __unicode__(self):
        return '%s - %s' % (self.hypothesis, self.date)