import os, sys
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(basedir))

import logging

import acs.db, acs.data

IMPORT_POPULATION_DATA = True
IMPORT_ZIP_CODE_DATA = True

# setup logging
logging.basicConfig(filename='world-cup.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("================================================================================")
logger.info("Importing ACS data:")

# create database
db = acs.db.CensusDataManager('sqlite:///acs.db')
logger.info("Connected to db")

if IMPORT_ZIP_CODE_DATA:
	logger.info("---------------------------------------------------------------------------")
	# load all the ZipCode data into memory
	dataset = acs.data.ZipCodeDataManager()
	logger.info("Loading ZipCode dataset from 'data' dir")
	dataset.loadFromCsv( 'data/zcta_tract_rel_10.csv' )
	# insert it all into a database
	db.emptyZipCodeTable()
	logger.info("Emptied Zip Code Table")
	total_records = len(dataset.records)
	last_pct = None
	done = 0
	logger.info("Importing into db ("+str(total_records)+" records)")
	for record in dataset.records:    
	    db.addZipCodeRecord(record)
	    done = done + 1
	    pct_done = round((float(done)/float(total_records))*100)
	    if (pct_done % 10 == 0) and (pct_done != last_pct):
	        logger.info("  "+str(pct_done)+'%')
	        last_pct = pct_done
	logger.info("  done")

if IMPORT_POPULATION_DATA:
	logger.info("---------------------------------------------------------------------------")
	# load all the ACS population data into memory
	dataset = acs.data.PopulationDataManager()
	logger.info("Loading Population dataset from 'data' dir")
	dataset.loadAllStateCsvs('data')
	logger.info("  done")
	# insert it all into a database
	db.emptyPopulationTable()
	logger.info("Emptied Population Table")
	total_records = len(dataset.records)
	last_pct = None
	done = 0
	logger.info("Importing into db ("+str(total_records)+" records)")
	for record in dataset.records:    
	    db.addPopulationRecord(record)
	    done = done + 1
	    pct_done = round((float(done)/float(total_records))*100)
	    if (pct_done % 10 == 0) and (pct_done != last_pct):
	        logger.info("  "+str(pct_done)+'%')
	        last_pct = pct_done
	logger.info("  done")
