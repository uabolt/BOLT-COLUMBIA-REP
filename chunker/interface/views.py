# -*- coding: utf-8 -*-
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
    
    # Get the next available ref/hyp pair
    ref = 'زوج أخته يتغل سايق سيارة' #request.Session['dataset'].pop(0)
    hyp = 'زوج أخته XXXX سايق سيارة'
    
    if request.method == 'POST':
        
        form = AnnotationForm(request.POST)
        if form.is_valid():
        	form.save()
        	messages.success(request, 'Annotation saved correctly.')

        else:
        	for error in form.errors:
        		messages.error(request, "%s: %s"%(error, form.errors[error]))
        		
        	return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp
    }))
		
    form = AnnotationForm(initial={'hypothesis':ref, 'reference':hyp})

    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp
    }))