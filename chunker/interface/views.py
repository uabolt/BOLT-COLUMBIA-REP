# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from interface.forms import POSAnnotationForm, RephAnnotationForm
from django.utils.translation import ugettext_lazy as _
import pdb


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def pos_annotation(request):

	# If the user already commited this answer, redirect it to the following page	
    if 'committed' in request.session:
        return HttpResponseRedirect(reverse('reph_annotation'))

    layout = 'horizontal'
    
    # Get the next available ref/hyp pair
    # ref = 'زوج أخته يتغل سايق سيارة' #request.Session['dataset'].pop(0)
#     hyp = 'زوج أخته _____ سايق سيارة'
#     ref_id = 'hola123'
#     sample_file = 'sample1.bin'

    dataset = request.session['dataset']
    sample = dataset[-1]
    ref = sample['ref']
    hyp = sample['chunked']
    ref_id = sample['id']
    sample_file = request.session['ds_file']
    
    if request.method == 'POST':
        
        form = POSAnnotationForm(request.POST)
        if form.is_valid():
			form.save()
			messages.success(request, 'POS Annotation saved correctly.')
			
			# Mark the session not to allow another commit of the answers
			request.session['committed'] = True
			return HttpResponseRedirect(reverse('reph_annotation'))
        else:
        	for error in form.errors:
        		messages.error(request, "%s: %s"%(error, form.errors[error]))
        		
        	return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp,
        'title': _('Guess'),
    }))
		
    form = POSAnnotationForm(initial={'masked':ref, 'reference':hyp, 'session_id':request.session.session_key, 'ref_id':ref_id, 'sample_file':sample_file})

    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp,
        'title': _('Guess'),
    }))
    
    
def reph_annotation(request):

    if not 'committed' in request.session:
	    return HttpResponseRedirect(reverse('pos_annotation'))

    layout = 'horizontal'
    
    # Get the next available ref/hyp pair
    # ref = 'زوج أخته يتغل سايق سيارة' #request.Session['dataset'].pop(0)
#     hyp = 'زوج أخته يتغل ساي[ق سيا]رة'
#     ref_id = 'hola123'
#     sample_file = 'sample1.bin'

    dataset = request.session['dataset']
    sample = dataset[-1]
    ref = sample['ref']
    hyp = sample['segmented']
    ref_id = sample['id']
    sample_file = request.session['ds_file']
    
    if request.method == 'POST':
        
        form = RephAnnotationForm(request.POST)
        if form.is_valid():
        	form.save()
        	messages.success(request, 'Rephrase Annotation saved correctly.')
        	
        	# Allow the user to proceed to the next instance
        	del request.session['committed']
        	request.session.modified = True
        	
        	# Persist the change in the session
        	dataset.pop()
        	request.session['dataset'] = dataset
        	
        	return HttpResponseRedirect(reverse('pos_annotation'))

        else:
        	for error in form.errors:
        		messages.error(request, "%s: %s"%(error, form.errors[error]))
        		
        	return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp,
        'title': _('Reprhase')
    }))
		
    form = RephAnnotationForm(initial={'segmented':ref, 'reference':hyp, 'session_id':request.session.session_key, 'ref_id':ref_id, 'sample_file':sample_file})

    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp,
        'title': _('Reprhase')
    }))