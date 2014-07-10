'''This script takes a file with the following format: "id buckwater-iraqi-sentence" and generates dataset files to be consumed by the UABOLT interface'''

import random as rnd
import subprocess

inputf = 'replication_dataset.romanized.sentids'
stopwf = 'BOLT.IA.Stopwords.20140702.txt'
out_prefix = 'ds_'

segmaxlen = 3
ds_len = 10
num_copies = 3

# First, build the stop words dictionary
sw = []

with open(stopwf, 'r') as f:
    for l in f:
        sw.append(l.split()[0])

# Now, generate the files
with open(inputf, 'r') as f:
    ix = 0

    for line in f:
        id, sentence = line.split(None, 1)

        #tokenize the sentence and proceed to error segment generation
        words = sentence.split()

        # If the sentence is a single word, we ignore it
        if len(words) <= segmaxlen:
            continue
        else:
            # Generate a random segment for this sentence
            allstopwords = True
            while allstopwords:
                offset = rnd.randint(0, len(words)-2)
                l = min(rnd.randint(1, segmaxlen), len(words)-offset)
                

                # Check wether the segment is composed only of stop words
                for word in words[offset:offset+l]:
                    if not word in sw: 
                        allstopwords = False
                        break

            # Map BUCKWATER to UTF-8
            pipe = subprocess.Popen(["perl", "./buckwalter2utf_sentids.prl", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            outs, errs = pipe.communicate(input=line)

            id, sentence = outs.split(None, 1)
            words = sentence.split()
            # Generate the actual data set lines
            ref = sentence
            chunked = ' '.join(words[0:offset]) 
            
            for i in range(l):
                chunked += ' _____ '

            chunked += ' '.join(words[offset+l:])

            segmented = ' '.join(words[0:offset])+ ' [' + ' '.join(words[offset:offset+l]) + '] '  + ' '.join(words[offset+l:])

            outline = '%s\t%s\t%s\t%s\t%i\n' % (id, ref, chunked, segmented, 0)
            
            # Open a new file if necessary
            if ix % ds_len == 0:
                try:
                    # Close the previous file, if exist
                    outf.close()
                except:
                    pass

                outfs = [open('%s%i_%i.ds' % (out_prefix, (ix+1)/ds_len, file_num), 'w') for file_num in range(num_copies)]

            for i in range(num_copies):
                outfs[i].write(outline)
            ix += 1


#Close the last open file
for i in range(num_copies):
    outfs[i].close()
    
