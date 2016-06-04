# Zika Papers

The objective of this project is to collect, organize and mine information from scientific papers discussing the Zika virus. This is an open science project. This means everybody is welcome (and encouraged) to contribute however they can, using whichever skills they have. Your contributions to the project will be recorded as comments in the issue tracker and pull requests to our repo. We will use those to automatically build a list of participants to give credit to everyone that helped.

# Minimum Viable Product (MVP)

Many of us can only work on this project in spare time, so we will take baby steps. The first MVP we are targetting is the collection and annotation of all scientific articles discussing Zika. First we will automatically extract entities and concepts mentioned in those articles. Subsequently, we will curate the extracted data to remove unrelated content and include missing entities/concepts.

# Design Decisions

I describe below a few design decisions to help you understand how we got where we got, but we're also open to constructive criticism and suggestions on how we can improve our project.

* Strong universal identifiers: 
  * currently using PMIDs in filenames because of initial focus on pubmed. We could use other IDs later as we progress.

* Reproducibility
  * as much as possible, I'd like for the code to work such that whoever downloads it can build all of the data files from scratch.
  * each step of the workflow is recorded in a file, so that we can easily inspect the output of each step

* Using a GNU Make as workflow manager. 
  * The Makefile specifies which scripts to run, in which order and on which input files.
  * If a given file is missing -- e.g. `simple/12345.json` -- running `make simple/12345.json` should call the right scripts with the right inputs to generate that file
  * If the workflow gets killed, running `make` again should pick up where it left
  * Easy parallelization by running `make -j <number of threads>` 

* Github issue tracker to coordinate development, issues, bugs, etc.

* Pull requests with diff patches to provide reproducible fixes to the data


