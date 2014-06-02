# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from interface.forms import POSAnnotationForm, RephAnnotationForm


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def pos_annotation(request):

    layout = 'horizontal'
    
    # Get the next available ref/hyp pair
    ref = 'زوج أخته يتغل سايق سيارة' #request.Session['dataset'].pop(0)
    hyp = 'زوج أخته _____ سايق سيارة'
    
    if request.method == 'POST':
        
        form = POSAnnotationForm(request.POST)
        if form.is_valid():
			form.save()
			messages.success(request, 'POS Annotation saved correctly.')
			return HttpResponseRedirect(reverse('reph_annotation'))
        else:
        	for error in form.errors:
        		messages.error(request, "%s: %s"%(error, form.errors[error]))
        		
        	return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp
    }))
		
    form = POSAnnotationForm(initial={'masked':ref, 'reference':hyp, 'session_id':request.session.session_key})

    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp
    }))
    
    
def reph_annotation(request):

    layout = 'horizontal'
    
    # Get the next available ref/hyp pair
    ref = 'زوج أخته يتغل سايق سيارة' #request.Session['dataset'].pop(0)
    hyp = 'زوج أخته يتغل ساي[ق سيا]رة'
    
    if request.method == 'POST':
        
        form = RephAnnotationForm(request.POST)
        if form.is_valid():
        	form.save()
        	messages.success(request, 'Rephrase Annotation saved correctly.')
        	
        	return HttpResponseRedirect(reverse('pos_annotation'))

        else:
        	for error in form.errors:
        		messages.error(request, "%s: %s"%(error, form.errors[error]))
        		
        	return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp
    }))
		
    form = RephAnnotationForm(initial={'rephrased':ref, 'reference':hyp, 'session_id':request.session.session_key})

    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp
    }))