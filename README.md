# Zika Papers

The objective of this project is to collect, organize and mine information from scientific papers discussing the Zika virus. This is an open science project. This means everybody is welcome (and encouraged) to contribute however they can, using whichever skills they have. Your contributions to the project will be recorded as comments in the issue tracker and pull requests to our repo. We will use those to automatically build a list of participants to give credit to everyone that helped.

# How to participate?

You can choose to help with whatever you're comfortable with:
* if you do not possess specialized scientific or engineering skills, you can help us find more material to add, or with many other tasks we may have (ask us!)
* if you are a health sciences professional, send questions you'd like us to answer, help us to curate the data and analyze the results
* if you are a data scientist, help us acquire + clean + mine the data
* if you are a software engineer or developer, help us to create or improve the code to support all of the above tasks
* if you are a designer, help us to do all of this with more efficacy and beauty!
* if you are a journalist, help us bring awareness to the project
* if you are the Zika Virus, tell us how exactly do you work and how we can coexist in peace


# Minimum Viable Product (MVP)

Many of us can only work on this project in spare time, so we will take baby steps. The first MVP we are targetting is the collection and annotation of all scientific articles discussing Zika. First we will automatically extract entities and concepts mentioned in those articles. Subsequently, we will curate the extracted data to remove unrelated content and include missing entities/concepts.


# Developer Quickstart

If you want to run/develop with us at this stage of the project, we assume you are running a Linux distribution (or at least MAC OS with add-ons). Let us know if that's not the case.

```
make install  # to install the prereqs
make all K=10 # to see the code running through the whole workflow with only 10 documents at first
make download # to download all of the content (900 abstracts)
make annotate # to run the workflow over the currently downloaded documents
```

# Design Decisions

I describe below a few design decisions to help you understand how we got where we got, but we're also open to constructive criticism and suggestions on how we can improve our project.

* Strong universal identifiers: 
  * currently using PMIDs in filenames because of initial focus on pubmed. We could use other IDs later as we progress;
  * tagging of scientific articles with references to knowledge bases through URIs so that we can potentially extract more background knowledge from those KBs.

* Reproducibility
  * as much as possible, I'd like for the code to work such that whoever downloads it can build all of the data files from scratch;
  * each step of the workflow is recorded in a file, so that we can easily inspect the output of each step;
  * errors are logged in a master errors.log so we can know when a given file didn't get correctly generated.

* Using a GNU Make as workflow manager:
  * the Makefile specifies which scripts to run, in which order and on which input files;
  * if a given file is missing -- e.g. `simple/12345.json` -- running `make simple/12345.json` should call the right scripts with the right inputs to generate that file;
  * if the workflow gets killed, running `make` again should pick up where it left;
  * easy parallelization by running `make -j <number of threads>`.

* Github issue tracker to coordinate development, issues, bugs, etc.

* Pull requests with diff patches to provide reproducible fixes to the data

