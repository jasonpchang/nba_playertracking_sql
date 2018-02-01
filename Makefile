####################################################
# Makefile for running code
####################################################

# definitions
S = ./src
D = ./dat

# keep intermediate files
.SECONDARY: 



########################################
# quick run
########################################
build:
	$S/scrape_nbaptmov.py 10-28-2014 10-28-2014 ./Dat/nbatracker.db 1

run:
	$S/read_movements.py ./Dat/nbatracker.db


# default rules
default: build
