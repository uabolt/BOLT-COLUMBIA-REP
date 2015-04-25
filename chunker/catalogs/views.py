from django.shortcuts import render
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.forms import ModelForm
from interface.models import POSAnnotation, RephAnnotation
from iraqiSpeakerVerifiers.models import SpeakerVerification
from .utils import seems_legit_answers
import chunker.settings as settings

# Create your views here.
class InterfaceListView(ListView):

    def get_queryset(self):
        ''' Grab the user_code (survey code) from the url as a parameter '''

        self.user_code = self.args[0].lower() # The first argument is the user_code
        model_class = self.model # Get the model to which it corresponds

        return model_class.objects.filter(user_code = self.user_code)

class HITListView(TemplateView):
    ''' This is not a ListView but rather displays a list of the HITs '''

    template_name = 'hit_list.html'

    def get_context_data(self, **kwargs):
        ''' Overriding the method '''

        # Perform the appropriate
        context = super(HITListView, self).get_context_data(**kwargs)

        # Retrieve the list of userc_codes and order it by date in decreasing order
        items = [i for i in POSAnnotation.objects.values('user_code', 'date', 'session_id').distinct() if i['user_code']] # Unique list of user_codes

        items = reversed(sorted(items, key=lambda x: x['date']))

        results = []

        # Fetch metadata
        for item in items:
            code = item['user_code']
            session_key = item['session_id']
            date = item['date']

            #code = code[4:] if code.startswith('SRI-') else code

            # Get the number of POS and REPH
            pos = POSAnnotation.objects.filter(user_code = code)
            reph = RephAnnotation.objects.filter(user_code = code)

            npos = len(pos)
            nreph= len(reph)

            # If the number of annotations is equal to the task size for both datasets, set the flag
            complete = npos == settings.TASK_SIZE and nreph == settings.TASK_SIZE

            # This flag is on if the answers seem legit
            seems_legit = seems_legit_answers(pos, reph)

            # Get the AMT id for the code

            try:
                amt_id = SpeakerVerification.objects.get(session_key = session_key).amt_id
            except Exception:
                amt_id = "N/A"

            results.append({'code':code, 'date':date, 'id':amt_id, 'complete':complete, 'legit':seems_legit})

        # Add it to the template context
        context['items'] = results

        # Finish
        return context

class ObjectTypeMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        ''' This is to add parameters without overriding this method in the views '''

        context = super(ObjectTypeMixin, self).get_context_data(**kwargs)
        context['obj_type'] = self.obj_type

        if hasattr(self, 'detail_url'):
            context['detail_url'] = self.detail_url

        return context

class POSListView(InterfaceListView, ObjectTypeMixin):

    template_name = 'catalog_list.html'
    obj_type = "POS annotations"
    model = POSAnnotation
    detail_url = 'hit-pos-detail'

class RephListView(InterfaceListView, ObjectTypeMixin):

    template_name = 'catalog_list.html'
    obj_type = "Reph annotations"
    model = RephAnnotation
    detail_url = 'hit-reph-detail'

class POSDetailView(DetailView, ObjectTypeMixin):

    template_name = 'catalog_detail.html'
    obj_type = "POS annotation"
    model = POSAnnotation

    class POSForm(ModelForm):
        class Meta:
            model = POSAnnotation

    def get_object(self):
        entity = super(POSDetailView, self).get_object()
        form = self.POSForm(instance=entity)

        return form

class RephDetailView(DetailView, ObjectTypeMixin):

    template_name = 'catalog_detail.html'
    obj_type = "Reph annotation"
    model = RephAnnotation

    class RephForm(ModelForm):
        class Meta:
            model = RephAnnotation

    def get_object(self):
        entity = super(RephDetailView, self).get_object()
        form = self.RephForm(instance=entity)

        return form
