import os, sys
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(basedir))

import logging

import acs.db, acs.data

# setup logging
logging.basicConfig(filename='world-cup.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("---------------------------------------------------------------------------")
logger.info("Importing ACS data:")

# create database
db = acs.db.CensusDataManager('sqlite:///acs.db')
logger.info("Connected to db")
db.empty()
logger.info("Emptied db")

# load all the ACS data
dataset = acs.data.ForeignBorn()
logger.info("Loading dataset from 'data' dir")
dataset.loadAllStateCsvs('data')
logger.info("  done")

# insert it all into a database
total_records = len(dataset.records)
last_pct = None
done = 0
logger.info("Importing into db ("+str(total_records)+" records)")
for record in dataset.records:    
    db.addRecord(record)
    done = done + 1
    pct_done = round((float(done)/float(total_records))*100)
    if (pct_done % 10 == 0) and (pct_done != last_pct):
        logger.info("  "+str(pct_done)+'%')
        last_pct = pct_done
logger.info("  done")
