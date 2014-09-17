# coding: utf-8
''' Extracts the RefAnnotations in a format suitable for AMU
 Run within the django shell '''

from interface.models import RephAnnotation
import pandas as pd

annotations = RephAnnotation.objects.all()

items = []
output_path = 'preliminar.csv'

series = [pd.Series({'ref_id':a.ref_id, 'reference':a.reference, 'hardness':a.hardness, 'local_rephrase':a.local_rephrase, 'local_merge':a.local_merge, 'global_rephrase':a.global_rephrase}) for a in annotations]
    
frame = pd.DataFrame(series)
frame.to_csv(output_path, encoding='utf_8', index=False, columns=['ref_id','reference', 'hardness', 'local_rephrase', 'local_merge', 'global_rephrase'])
