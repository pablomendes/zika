import sys
import json
import logging
import itertools
from collections import Counter
import re
logging.basicConfig(format='%(levelname)s:%(filename)s:%(message)s',filename='errors.log',level=logging.ERROR)

input_filename = sys.argv[1]
output_filename = sys.argv[2]
topk = 200
if len(sys.argv)>3:
    topk=sys.argv[3]

def clean(s):
    return s.replace("http://dbpedia.org/resource/","")

with open(input_filename,'r') as f_in, open(output_filename, 'w') as f_out:
    nodes = Counter()
    links = list() 
    wspace = re.compile("[\s\t]+")
    k = 0
    i = 0
    for line in file.readlines(f_in):
        k += 1
        if k==topk:
            break
        try:
            f = line.split()
            v,e1,e2 = f
            if e1 not in nodes:
                nodes[e1]=i
                i+=1
            if e2 not in nodes:
                nodes[e2]=i
                i+=1
            links.append({"value": v, "source": nodes[e1], "target": nodes[e2]})
        except ValueError:
            logging.error("Could not parse line: %s" % line)
        
    #TODO group by type? by how frequent? by "relevance" as specified manually by the community?
    grouped_nodes = [ { "group": 1, "name": clean(n) } for n in nodes ]
    f_out.write(json.dumps({"links": links, "nodes": grouped_nodes}))

