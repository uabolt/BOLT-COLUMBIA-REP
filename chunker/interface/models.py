from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class POSAnnotation(models.Model):
    '''Class that represents an annotation for the replica of Columbia's experiment in IA'''

    POS_TAGS = (
        ('C', _('Coordinating conjunction')),
        ('D', _('Cardinal number')),
        ('DT', _('Determiner')),
        ('EX', _('Existential there')),
        ('FW', _('Foreign word')),
        ('IN', _('Preposition or subordinating conjunction')),
        ('JJ', _('Adjective')),
        ('JJR', _('Adjective, comparative')),
        ('JJS', _('Adjective, superlative')),
        ('LS', _('List item marker')),
        ('MD', _('Modal')),
        ('NN', _('Noun, singular or mass')),
        ('NNS', _('Noun, plural')),
        ('NNP', _('Proper noun, singular')),
        ('NNPS', _('Proper noun, plural')),
        ('PDT', _('Predeterminer')),
        ('POS', _('Possessive ending')),
        ('PRP', _('Personal pronoun')),
        ('PRP$', _('Possessive pronoun')),
        ('RB', _('Adverb')),
        ('RBR', _('Adverb, comparative')),
        ('RBS', _('Adverb, superlative')),
        ('RP', _('Particle')),
        ('SYM', _('Symbol')),
        ('TO', _('to')),
        ('UH', _('Interjection')),
        ('VB', _('Verb, base form')),
        ('VBD', _('Verb, past tense')),
        ('VBG', _('Verb, gerund or present participle')),
        ('VBN', _('Verb, past participle')),
        ('VBP', _('Verb, non-3rd person singular present')),
        ('VBZ', _('Verb, 3rd person singular present')),
        ('WDT', _('Wh-determiner')),
        ('WP', _('Wh-pronoun')),
        ('WP$', _('Possessive wh-pronoun')),
        ('WRB', _('Wh-adverb')),
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
    legible = models.BooleanField(blank=False) # Is the sentence legible despite the missing chunks?
    guess = models.CharField(blank=True, max_length=50) # The guessed word, or blank if can't be guessed
    POS = models.CharField(blank=True, choices=POS_TAGS, max_length=7) # Part of speech tag of the guessed word
    question = models.CharField(blank=True, max_length=300) # Targeted question/definition to obtain the missing word

    

    def __unicode__(self):
        return '%s - %s' % (self.masked, self.date)
        
class RephAnnotation(models.Model):
    '''Class that represents an annotation for the replica of AMU's experiment in IA'''

    # Scale goes from easy to hard incrementaly
    EASINESS_CHOICES = (
        (1, _('Very easy')),
        (2, _('Easy')),
        (3, _('More or less')),
        (4, _('Hard')),
        (5, _('Very hard')),
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
    hardness = models.IntegerField(default=3, choices=EASINESS_CHOICES) # How hard is it to rephrase
    local_rephrase = models.CharField(blank=True, max_length=75) # Local rephrase
    reph_type = models.IntegerField(blank=True, null=True, choices=REPHRASE_CHOICES) # What kind of answer is this
    local_merge = models.CharField(blank=True, max_length=255) # Local rephrase merged with the hyp
    global_rephrase = models.CharField(blank=True, max_length=255) # Rephrased sentences
    
    def __unicode__(self):
        return '%s - %s' % (self.segmented, self.date)