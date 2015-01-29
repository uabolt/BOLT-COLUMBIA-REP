# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from interface.forms import POSAnnotationForm, RephAnnotationForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from models import POSTag
from iraqiSpeakerVerifiers.models import SpeakerVerification
import pdb


# Create your views here.

def instructions(request):
    return render_to_response('instructions.html', RequestContext(request, {'lang':'arabic' if settings.LANGUAGE_CODE == 'ar-iq' else 'english',}))

def pos_annotation(request):

    # If the user already commited this answer, redirect it to the following page   
    if 'committed' in request.session:
        return HttpResponseRedirect(reverse('reph_annotation'))

    layout = 'horizontal'

    dataset = request.session['dataset']
    sample = dataset[-1]
    ref = sample['ref']
    hyp = sample['chunked']
    ref_id = sample['id']
    sample_file = request.session['ds_file']
    user_code = request.session['user_code']

    if request.method == 'POST':
        
        form_annotation = POSAnnotationForm(request.POST)

        if form_annotation.is_valid():

            form_annotation.save()
            messages.success(request, _('POS Annotation saved correctly.'))
            
            # Number of POS tags
            num_pos = int(request.POST['num_pos']) if 'num_pos' in request.POST else 1
        
            pos_tags = [] # List to hold the POS tags
       
            for i in range(1, num_pos+1):
                tag = POSTag()
                tag.POS = request.POST['POS_%s' % i]
                tag.annotation = form_annotation.instance
                tag.save()
            
            # Mark the session not to allow another commit of the answers
            request.session['committed'] = True
            return HttpResponseRedirect(reverse('reph_annotation'))
        else:
            for error in form_annotation.errors:
                messages.error(request, "%s: %s"%(error, form_annotation.errors[error]))
                
            return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form_annotation,
        'layout': layout,
        'hyp':hyp,
        'title': _('Guess'),
    }))
        
    form_annotation = POSAnnotationForm(initial={'masked': ref, 'reference': hyp,
                                                 'session_id': request.session.session_key, 'user_code': user_code,
                                                 'ref_id': ref_id, 'sample_file': sample_file})

    return render_to_response('form_pos.html', RequestContext(request, {
        'form': form_annotation,
        'lang':'arabic' if settings.LANGUAGE_CODE == 'ar-iq' else 'english',  
        'layout': layout,
        'hyp':hyp,
        'title': _('Guess'),
        'pos_tags': POSTag.POS_TAGS,
    }))
    
    
def reph_annotation(request):

    if not 'committed' in request.session:
        return HttpResponseRedirect(reverse('pos_annotation'))

    layout = 'horizontal'

    dataset = request.session['dataset']
    sample = dataset[-1]
    ref = sample['ref']
    hyp = sample['segmented']
    ref_id = sample['id']
    sample_file = request.session['ds_file']
    user_code = request.session['user_code']


    if request.method == 'POST':
        
        form = RephAnnotationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Rephrase Annotation saved correctly.'))
            
            # Allow the user to proceed to the next instance
            del request.session['committed']
            request.session.modified = True
            
            # Persist the change in the session
            dataset.pop()
            request.session['dataset'] = dataset

            if len(dataset) > 0:
                return HttpResponseRedirect(reverse('pos_annotation'))
            else:
                return HttpResponseRedirect(reverse('finish'))

        else:
            for error in form.errors:
                messages.error(request, "%s: %s"%(error, form.errors[error]))
                
            return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
        'hyp':hyp,
        'title': _('Reprhase')
    }))
        
    form = RephAnnotationForm(initial={'segmented': ref, 'reference': hyp, 'session_id': request.session.session_key,
                                       'user_code': user_code, 'ref_id': ref_id, 'sample_file': sample_file})

    return render_to_response('form_reph.html', RequestContext(request, {
        'form': form,
        'lang':'arabic' if settings.LANGUAGE_CODE == 'ar-iq' else 'english',  
        'layout': layout,
        'hyp':hyp,
        'title': _('Reprhase')
    }))
