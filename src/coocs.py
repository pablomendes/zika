import sys
import json
import spotlight
import logging
import itertools
logging.basicConfig(format='%(levelname)s:%(filename)s:%(message)s',filename='errors.log',level=logging.ERROR)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

with open(input_filename,'r') as f_in, open(output_filename, 'w') as f_out:
    annotations = file.read(f_in)
    entities = annotations.strip().split('\n') 

    pairs = set()
    for i in range(0,len(entities)):
        for j in range(i+1,len(entities)):
            pair = [entities[i],entities[j]]
            pair.sort()
            pairs.add("\t".join(pair))
    
    f_out.write("\n".join(pairs))
    f_out.write("\n")

