import sys
import json
import spotlight
import logging
logging.basicConfig(format='%(levelname)s:%(filename)s:%(message)s',filename='errors.log',level=logging.ERROR)


LANG_PORTS = {
    "english": '2222',
    "german": '2226',
    "dutch": '2232',
    "hungarian": '2229',
    "french": '2225',
    "portuguese": '2228',
    "italian": '2230',
    "russian": '2227',
    "turkish": '2235',
    "spanish": '2231'
}

port = LANG_PORTS["english"]
url ="http://spotlight.sztaki.hu:%s/rest/annotate" % port

input_filename = sys.argv[1]
output_filename = sys.argv[2]

text = "This is a test with Berlin"
with open(input_filename,'r') as f_in, open(output_filename, 'w') as f_out:
    article = json.load(f_in)
    text = article["title"] + " \n " + article["abstract"]

    try:
        annotations = spotlight.annotate( url, text, spotter="Default", disambiguator="Default", confidence=0.5, support=0)
    except Exception, e:
        logging.error("%s %s" % (input_filename, str(e)))
        annotations = []
    json.dump(annotations, f_out, indent=2)
