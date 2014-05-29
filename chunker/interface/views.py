from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from interface.forms import AnnotationForm


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def annotation(request):
    #messages.success(request, 'I am a success message.')

    layout = 'horizontal'
    if request.method == 'POST':
        form = AnnotationForm(request.POST)
        form.is_valid()
    else:
        form = AnnotationForm()

    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))