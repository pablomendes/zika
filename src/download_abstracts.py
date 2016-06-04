from Bio import Entrez
import json
import argparse
import traceback
import logging
logging.basicConfig(filename='errors.log',level=logging.ERROR)

def search(query,k=10):
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax=k,
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

def parse_book(metadata):
    doctype = 'BookDocument'
    pmid = metadata[doctype]['PMID']
    abstract = ""
    if "Abstract" in metadata[doctype]:
        abstract = u'\n'.join(metadata[doctype]['Abstract']['AbstractText'])
    title = metadata[doctype]['Book']['BookTitle']
    parsed = {'pmid': pmid, 'title': title, 'abstract': abstract, 'doctype': doctype}
    return parsed

def parse_article(metadata):
    doctype = 'MedlineCitation'
    paper = metadata[doctype]['Article']
    pmid = metadata[doctype]['PMID']
    abstract = ""
    if "Abstract" in paper:
        abstract = u'\n'.join(paper['Abstract']['AbstractText'])
    title = paper['ArticleTitle']
    parsed = {'pmid': pmid, 'title': title, 'abstract': abstract, 'doctype': doctype}
    return parsed

def parse(metadata):
    if 'BookDocument' in metadata:
        doctype = 'BookDocument'
        parsed = parse_book(metadata)
    elif 'MedlineCitation' in metadata:
        doctype = 'MedlineCitation'
        parsed = parse_article(metadata)
    else:
        msg = "No MedlineCitation or BookDocument in metadata: %s" % (json.dumps(metadata))
        raise Exception(msg)
    return parsed
 
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="max num of abstracts to download", default="zika")
    parser.add_argument("-k", "--retmax", help="max num of abstracts to download", default=10)
    args = parser.parse_args()

    Entrez.email = 'pablomendes@gmail.com'
    results = search(args.query, args.retmax) #879
    id_list = results['IdList']
    papers = fetch_details(id_list)
    
    for i, metadata in enumerate(papers):
        try:
            parsed = parse(metadata)
            pmid = parsed['pmid'] 
            with open("orig/"+pmid+".json","w") as f_orig, open("simple/"+pmid+".json","w") as f_simple: #, open("errors/"+pmid+".error","w") as f_error :

                print("%d: (%s) %s" % (i, pmid, parsed['title']))

                #try:
                f_simple.write(json.dumps(parsed, indent=2, separators=(',', ':')))
                f_orig.write(json.dumps(metadata, indent=2, separators=(',', ':')))
                #except:
                #    logging.error("%d: %s" % (i+1, traceback.print_exception()))
                #    traceback.print_stack(file=f_error)
        except Exception, e:
            msg = "Can't parse %d: %s" % (i, json.dumps(metadata))
            print("%d. %s: %s" % (i, "Can't parse metadata.", str(e)))
            logging.error(msg)
            continue
        

