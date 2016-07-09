import sys
import json
import logging
import itertools
from collections import Counter
import re
logging.basicConfig(format='%(levelname)s:%(filename)s:%(message)s',filename='errors.log',level=logging.ERROR)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

def clean(s):
    return s.replace("http://dbpedia.org/resource/","")

with open(input_filename,'r') as f_in, open(output_filename, 'w') as f_out:
    nodes = Counter()
    links = list() 
    wspace = re.compile("[\s\t]+")
    for line in file.readlines(f_in):
        try:
            f = line.split()
            v,e1,e2 = f
            nodes[e1] += int(v)
            nodes[e2] += int(v)
            links.append({"value": v, "source": clean(e1), "target": clean(e2)})
        except ValueError:
            logging.error("Could not parse line: %s" % line)
    #TODO group by type? by how frequent? by "relevance" as specified manually by the community?
    grouped_nodes = [ {"group": 1, "name": n} for n in nodes ]
    f_out.write(json.dumps({"links": links, "nodes": grouped_nodes}))

