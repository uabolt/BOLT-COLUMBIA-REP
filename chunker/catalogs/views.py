from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from interface.models import POSAnnotation, RephAnnotation
from iraqiSpeakerVerifiers.models import SpeakerVerification

# Create your views here.
class InterfaceListView(ListView):

    def get_queryset(self):
        ''' Grab the user_code (survey code) from the url as a parameter '''

        self.user_code = self.args[0].lower() # The first argument is the user_code
        model_class = self.model # Get the model to which it corresponds

        return model_class.objects.filter(user_code = self.user_code)



class POSListView(InterfaceListView):
    model = POSAnnotation

class RephListView(InterfaceListView):
    model = RephAnnotation

class POSDetailView(DetailView):
    model = POSAnnotation

class RephDetailView(DetailView):
    model = RephAnnotation

class HITListView(TemplateView):
    ''' This is not a ListView but rather displays a list of the HITs '''

    def get_context_data(self, **kwargs):
        ''' Overriding the method '''

        # Perform the appropriate
        context = super(HITListView, self).get_context_data(**kwargs)

        # Retrieve the list of userc_codes
        codes = [i[0] for i in SpeakerVerification.objects.order_by('-pk').values_list('user_code')]

        # Add it to the template context
        context['user_codes'] = codes

        # Finish
        return context
