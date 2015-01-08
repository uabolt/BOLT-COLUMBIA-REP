from django.forms import ModelForm
import django.forms as forms
from django.utils.translation import ugettext_lazy as _
from interface import models

class POSAnnotationForm(ModelForm):
	
                
	class Meta:
		model = models.POSAnnotation
		fields = '__all__'
		widgets = {
		    'masked': forms.HiddenInput(),
		    'reference': forms.HiddenInput(),
		    'control_annotation': forms.HiddenInput(),
		    'date': forms.HiddenInput(),
			'session_id': forms.HiddenInput(),
			'legible': forms.Select(choices = [(False, _('No')), (True, _('Yes'))]), 
			'ref_id': forms.HiddenInput(),
			'sample_file': forms.HiddenInput()
		}
		
		labels = {
			'legible' : _('Legible'),
			'guess' : _('Guess'),
			'question' : _('Question'),
			'POS': _('Part of speech'),
            'continue_process': _('Continue the process'),
		}
		
		help_texts = {
			'legible': _('Can you understand the meaning of the sentence?'),
			'guess' : _('Try to guess the words that fit into the ____ place if possible'),
			'question' : _('What would you ask the speaker (or author) of the sentence in order to identify what the missing words are?  Please type your question here.'),
			'POS': _('Select the part of speech you believe that the ____ word is (e.g. Noun)'),
            'continue_process':_('Would you stop and ask a question'),
		}
		
class RephAnnotationForm(ModelForm):
	class Meta:
		model = models.RephAnnotation
		fields = '__all__'
		widgets = {
		    'segmented': forms.HiddenInput(),
		    'reference': forms.HiddenInput(),
		    'session_id': forms.HiddenInput(),
		    'control_annotation': forms.HiddenInput(),
		    'date': forms.HiddenInput(),
			'local_merge': forms.Textarea(),
			'global_rephrase': forms.Textarea(),
			'ref_id': forms.HiddenInput(),
			'sample_file': forms.HiddenInput()
		}
		
		labels = {
			'hardness': _('Hardness'),
			'local_rephrase': _('Local rephrease'),
			'reph_type' : _('Rephrase type'),
			'local_merge' : _('Merged sentence'),
			'global_rephrase' : _('Rephrase the complete sentence'),
		}
		
		help_texts = {
			'hardness': _('How hard do you think the missing word or words are to rephrase'),
			'local_rephrase': _('Try to provide a rephrase ONLY of the text within brakets. If rephrasing is too difficult, try to describe or define what the missing text means'),
			'local_merge' : _('Try to merge your rephrased text into the original sentence, making minimal changes to the original sentence'),
			'reph_type' : _("Did you provide a 'rephrase' (rewriting the red text in different words) or a 'definition' (a description of what the words are, but not something you could insert with the rest of the sentence)?"),
			'global_rephrase' : _('Please provide an alternate rephrasing of the original sentence'),
			
		}
		
		
