''' This script deletes blank reph annotations from the database'''

from interface.models import RephAnnotation

# Get the empty reph annotations
entries = RephAnnotation.objects.filter(local_rephrase = '').filter(local_merge = '').filter(global_rephrase = '')

num = len(entries)
# Delete them
for entry in entries:
  entry.delete()

print 'Deleted %i entries' % num
