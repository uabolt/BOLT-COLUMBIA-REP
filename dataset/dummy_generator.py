#!/usr/bin/python
'''Just generates dummy dataset from unicode sentence files'''

import sys

i = 1
for line in sys.stdin:
    line = line[:-1]
    print '%i\t%s\t%s\t%s\t0' % (i, line, line, line)
    i += 1