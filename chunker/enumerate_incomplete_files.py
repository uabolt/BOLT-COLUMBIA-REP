''' Script that enumerate the files that have less than 10 of its elements annotated'''

from interface.models import RephAnnotation, DatasetAssignment
from django.db.models import Count

# Make the aggregation
file_elements = RephAnnotation.objects.values('sample_file').annotate(elements=Count('sample_file'))

# Print the file names for those file with less than 10 elements
for e in file_elements:
    if e['elements'] < 10:
        print e['sample_file']
