K=900
ORIG_FILES=$(wildcard orig/*.json)
SIMPLE_JSON_FILES=$(wildcard simple/*.json)

all:setup download parse annotate patch

setup:
	mkdir -p orig simple spotlight-output spotlight-output-patches

# parsing depends on downloading (currently jointly executed)
parse:download
	# currently the parsing is done at the same time as the download

# annotating depends on downloading, parsing and running annotation on every parsed file
annotate:parse $(SIMPLE_JSON_FILES:simple/%.json=spotlight-output/%.json)

entities:$(SIMPLE_JSON_FILES:simple/%.json=spotlight-output/%.eset)

spotlight-output/%.eset:spotlight-output/%.json
	cat $< | jq -r ".[].URI" | sort -u > $@

stats/entity_counts.csv:entities
	echo "age,population" > $@
	cat spotlight-output/*.eset | sort | grep -v "," | uniq -c | sort -nr | sed -E "s|[ ]+([0-9]+) http://dbpedia.org/resource/(.+)|\2,\1|" | head -10 >> $@

#TODO patching depends on downloading, parsing, annotating and manually generated patch files to be applied in order
patch:annotate

download:
	python src/download_abstracts.py --retmax $(K)

install:
	pip install -r requirements.txt
	mkdir -p orig simple spotlight-output
	brew install jq
	apt-get install jq

spotlight-output/%.json:simple/%.json
	python src/annotate.py $< $@
    
clean:
	mkdir -p bak
	mv errors.log bak/errors.log.`date +%F_%R`
