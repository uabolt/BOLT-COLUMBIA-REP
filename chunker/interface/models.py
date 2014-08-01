from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class POSAnnotation(models.Model):
    '''Class that represents an annotation for the replica of Columbia's experiment in IA'''

    LEGIBLENESS_CHOICES = (
        (2, "---------"),
        (0, _("No")),
        (1, _("Yes")),
    )


    # Control fields
    ref_id = models.CharField(blank=False, max_length=50) # Sentence ID
    sample_file = models.CharField(blank=False, max_length=255) # File from which this sample forms part
    masked = models.CharField(blank=False, max_length=255) # Ref without some chunks
    reference = models.CharField(blank=False, max_length=255) # The ref
    control_annotation = models.BooleanField(blank=False) # If this is true, then this annotation is used for control purposes
    date = models.DateField(auto_now_add=True)
    session_id = models.CharField(blank=False, max_length=80) # Here goes the session ID

    # Columbia experiment's fields
    legible = models.IntegerField(default=2, choices=LEGIBLENESS_CHOICES)
    guess = models.CharField(blank=True, max_length=50) # The guessed word, or blank if can't be guessed
    question = models.CharField(blank=True, max_length=300) # Targeted question/definition to obtain the missing word

    

    def __unicode__(self):
        return '%s - %s' % (self.masked, self.date)
        
class RephAnnotation(models.Model):
    '''Class that represents an annotation for the replica of AMU's experiment in IA'''

    # Scale goes from easy to hard incrementaly
    EASINESS_CHOICES = (
        (1, "----------"),
        (2, _('Very easy')),
        (3, _('Easy')),
        (4, _('More or less')),
        (5, _('Hard')),
        (6, _('Very hard')),
    )

    REPHRASE_CHOICES = (
        (0, _('Rephrase')),
        (1, _('Definition')),
    )

	# Control fields
    ref_id = models.CharField(blank=False, max_length=50) # Sentence ID
    sample_file = models.CharField(blank=False, max_length=255) # File from which this sample forms part
    segmented = models.CharField(blank=False, max_length=255) # Ref without some chunks
    reference = models.CharField(blank=False, max_length=255) # The ref
    control_annotation = models.BooleanField(blank=False) # If this is true, then this annotation is used for control purposes
    date = models.DateField(auto_now_add=True)
    session_id = models.CharField(blank=False, max_length=80) # Here goes the session ID

	# Rephrase fields
    hardness = models.IntegerField(default=1, choices=EASINESS_CHOICES) # How hard is it to rephrase
    local_rephrase = models.CharField(blank=True, max_length=75) # Local rephrase
    reph_type = models.IntegerField(blank=True, null=True, choices=REPHRASE_CHOICES) # What kind of answer is this
    local_merge = models.CharField(blank=True, max_length=255) # Local rephrase merged with the hyp
    global_rephrase = models.CharField(blank=True, max_length=255) # Rephrased sentences
    
    def __unicode__(self):
        return u'%s - %s' % (self.segmented, self.date)
        
class POSTag(models.Model):
    
    POS_TAGS = (
        ('', '-----'),
        ('C', _('Coordinating conjunction')),
        ('D', _('Cardinal number')),
        #('DT', _('Determiner')),
        #('EX', _('Existential there')),
        ('FW', _('Foreign word')),
        #('IN', _('Preposition or subordinating conjunction')),
        ('JJ', _('Adjective')),
        #('JJR', _('Adjective, comparative')),
        #('JJS', _('Adjective, superlative')),
        ('MD', _('Modal')),
        ('NN', _('Noun, singular or mass')),
        #('NNS', _('Noun, plural')),
        ('NNP', _('Proper noun, singular')),
        #('NNPS', _('Proper noun, plural')),
        ('PRP', _('Personal pronoun')),
        #('PRP$', _('Possessive pronoun')),
        ('RB', _('Adverb')),
        #('RBR', _('Adverb, comparative')),
        #('RBS', _('Adverb, superlative')),
        #('RP', _('Particle')),
        ('SYM', _('Symbol')),
        #('TO', _('to')),
        #('UH', _('Interjection')),
        ('VB', _('Verb, base form')),
        #('VBD', _('Verb, past tense')),
        #('VBG', _('Verb, gerund or present participle')),
        #('VBN', _('Verb, past participle')),
        #('VBP', _('Verb, non-3rd person singular present')),
        #('VBZ', _('Verb, 3rd person singular present')),
    )
    
    annotation = models.ForeignKey(POSAnnotation)
    POS = models.CharField(blank=True, choices=POS_TAGS, max_length=7) # Part of speech tag of the guessed word
    
    def __unicode__(self):
        return u'%s - %s' % (self.annotation, self.POS)

    
    

class DatasetAssignment(models.Model):

    session_id = models.CharField(blank=False, max_length=80) # Here goes the session ID
    file_prefix = models.CharField(blank=False, max_length=10) # Here goes the file prefix to ensure the same dataset doesn't appear to the same user session
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s' % (self.session_id, self.file_prefix)
