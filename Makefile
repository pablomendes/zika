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

#TODO patching depends on downloading, parsing, annotating and manually generated patch files to be applied in order
patch:annotate

download:
	python src/download_abstracts.py --retmax $(K)

install:
	pip install -r requirements.txt
	mkdir -p orig simple spotlight-output

spotlight-output/%.json:simple/%.json
	python src/annotate.py $< $@
    
clean:
	mkdir -p bak
	mv errors.log bak/errors.log.`date +%F_%R`
