K=900
ORIG_FILES=$(wildcard orig/*.json)
SIMPLE_JSON_FILES=$(wildcard simple/*.json)

install:
	pip install -r requirements.txt
	mkdir -p orig simple spotlight-output spotlight-output-patches spotlight-postproc stats

all: download parse annotate patch

download:
	python src/download_abstracts.py --retmax $(K)

# parsing depends on downloading (currently jointly executed)
parse:download
	# currently the parsing is done at download time

# annotating depends on downloading, parsing and running annotation on every parsed file
annotate:parse $(SIMPLE_JSON_FILES:simple/%.json=spotlight-output/%.json)

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

pairs:$(SIMPLE_JSON_FILES:simple/%.json=spotlight-postproc/%.pairs)

spotlight-postproc/%.pairs:spotlight-postproc/%.eset
	python src/coocs.py $< $@

stats/pair_counts.csv:pairs
	cat spotlight-postproc/*.pairs | sort | uniq -c | sort -nr > $@

clean:
	mkdir -p bak
	mv errors.log bak/errors.log.`date +%F_%R`
