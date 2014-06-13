from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
import glob, random, os, shutil, re, pdb

pattern = re.compile(r'^/admin/?')

class AssignDataset:
    
    def process_request(self, request):
        ''' Assigns a dataset to the session if it doesn't exist yet. This middleware should go after the session middleware'''
        
        #if not pattern.match(request.path) and not reverse('finish') in request.path and not reverse('instructions') in request.path:
        if reverse('pos_annotation') in request.path or reverse('reph_annotation') in request.path:
            path = settings.DATASET_DIR
        
            # Dataset should be a non empty sequence on the
            if not 'dataset' in request.session or len(request.session['dataset']) == 0:
            
                # Retrieve the dataset files
                files = glob.glob(os.path.join(path, "*.ds"))
                
                if len(files) == 0:
                    return HttpResponseRedirect(reverse('finish'))
            
                # Generate a random index
                ix = random.randint(0, len(files)-1)
            
                # Read the contents
                with open(files[ix], 'r') as f:
                    fields = ('id', 'ref', 'chunked', 'segmented', 'control')
                    sentences = []
                    # Each line has format "id \t ref \t chunked \t segmented \t control(boolean field)
                    for line in f:
                        sentences.append(dict(zip(fields, line.split('\t'))))
                    
                request.session['dataset'] = sentences
                request.session['ds_file'] = files[ix].split('/')[-1] # Last token, which is the actual file name
            
                # Move the file to the processed files folder
                path = os.path.join(path, 'processed')
                if not os.path.exists(path):
                    os.makedirs(path)
            
                shutil.move(files[ix], path)
        
        
        return None
        
        
