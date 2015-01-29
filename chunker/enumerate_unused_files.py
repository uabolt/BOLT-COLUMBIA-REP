''' Script that enumerates the files that have been assigned but not worked in '''

from interface.models import RephAnnotation
from interface.models import DatasetAssignment

# Get the datasets assigned
assigned_files = set(a.file_prefix for a in DatasetAssignment.objects.all())

# Get the files that have gone at least one element through
worked_files = set(a.sample_file[:-3] for a in RephAnnotation.objects.all())

# Generate the difference
files = [x+".ds" for x in assigned_files - worked_files]

# Print the files 
for f in files: print f

# Maybe delete the dataset assignments
choice = raw_input('Delete the assignments from the database? y/[n]')

if choice == 'y':
    dsas = DatasetAssignment.objects.filter(file_prefix__in = assigned_files - worked_files)
    for dsa in dsas:
        dsa.delete()

    print "Assignments deleted."
