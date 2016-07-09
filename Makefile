K=900
ORIG_FILES=$(wildcard orig/*.json)
SIMPLE_JSON_FILES=$(wildcard simple/*.json)

install:
	pip install -r requirements.txt
	mkdir -p orig simple spotlight-output spotlight-output-patches spotlight-postproc stats

all: download parse annotate patch

download:
	python src/download_abstracts.py -q zika --retmax $(K)
	python src/download_abstracts.py -q microcephaly --retmax $(K)
	#python src/download_abstracts.py -q "aedes aegypti" --retmax $(K)
	python src/download_abstracts.py -q pyriproxyfen --retmax $(K)

# parsing depends on downloading (currently jointly executed)
parse:download
	# currently the parsing is done at download time

# annotating depends on downloading, parsing and running annotation on every parsed file
annotate:$(SIMPLE_JSON_FILES:simple/%.json=spotlight-output/%.json)

spotlight-output/%.json:simple/%.json
	python src/annotate.py $< $@

# extracting entities from the annotations
entities:$(SIMPLE_JSON_FILES:simple/%.json=spotlight-postproc/%.eset)

spotlight-postproc/%.eset:spotlight-output/%.json
	cat $< | jq -r ".[].URI" | sort -u > $@

#TODO patching depends on downloading, parsing, annotating and manually generated patch files to be applied in order
patch: annotate
	#TODO implement patching
   
stats/entity_counts.csv:entities
	echo "age,population" > $@
	#TODO this is currently Mac-specific. #FIXME
	cat spotlight-postproc/*.eset | sort | grep -v "," | uniq -c | sort -nr | sed -E "s|[ ]+([0-9]+) http://dbpedia.org/resource/(.+)|\2,\1|" | head -10 >> $@

coocs:$(SIMPLE_JSON_FILES:simple/%.json=spotlight-postproc/%.coocs)

spotlight-postproc/%.coocs:spotlight-postproc/%.eset
	python src/coocs.py $< $@

stats/cooc_counts.csv:$(SIMPLE_JSON_FILES:simple/%.json=spotlight-postproc/%.coocs)
	cat spotlight-postproc/*.coocs | sort | uniq -c | sort -nr > $@

stats/cooc_counts.json:stats/cooc_counts.csv
	python src/coocs2json.py $< $@

clean:
	mkdir -p bak
	mv errors.log bak/errors.log.`date +%F_%R`
