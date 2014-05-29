from django.forms import ModelForm
import django.forms as forms
from django.utils.translation import ugettext_lazy as _
from interface import models

class AnnotationForm(ModelForm):
	
                
	class Meta:
		model = models.Annotation
		fields = '__all__'
		widgets = {
		    'hypothesis': forms.HiddenInput(),
		    'reference': forms.HiddenInput(),
		    'control_annotation': forms.HiddenInput(),
		    'date': forms.HiddenInput(),
			'local_merge': forms.Textarea(),
			'global_rephrase': forms.Textarea(),
			'legible': forms.Select(choices = [(True, 'Yes'), (False, 'No')])
		}
		
		labels = {
			'legible' : _('Legible'),
			'guess' : _('Guess'),
			'question' : _('Question'),
			'POS': _('Part of speech'),
			'eassines': _('Eassines'),
			'local_rephrase': _('Local rephrease'),
			'reph_type' : _('Rephrase type'),
			'local_merge' : _('Merged sentence'),
			'global_rephrase' : _('Rephrase the complete sentence'),
		}
		
		help_texts = {
			'legible': _('Can you understand the meaning of the sentence?'),
			'guess' : _('Try to guess the words that fit into the XXXX place if possible'),
			'question' : _('Try to provide a targeted question to retrieve the missing words if possible'),
			'POS': _('Select the part of speech you believe that the XXX word is (i.e. Noun)'),
			'eassines': _('How hard do you think the missing word or words are to rephrase'),
			'local_rephrase': _('Try to provide a rephrase ONLY of the missing words. If it\'s too hard, provide a definition if possible'),
			'local_merge' : _('Retype the sentence with your local rephrase, if possible'),
			'reph_type' : _('Specify your rephrase type'),
			'global_rephrase' : _('Try to rephrase the complete sentence'),
			
		}
		
		