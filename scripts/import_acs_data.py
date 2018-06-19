import logging
import os

from ourcup import db
from ourcup.acs.population import PopulationDataManager
from ourcup.acs.zip_code import ZipCodeDataManager

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMPORT_ZIP_CODE_DATA = True
IMPORT_POPULATION_DATA = True

# setup logging
logging.basicConfig(format="[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("================================================================================")
logger.info("Importing data:")

if IMPORT_ZIP_CODE_DATA:
    # this can take 5 minutes or so
    logger.info("---------------------------------------------------------------------------")
    # load all the ZipCode data into memory
    dataset = ZipCodeDataManager()
    logger.info("Loading ZipCode dataset from 'data' dir")
    dataset.loadFromCsv(os.path.join(basedir, 'data', 'zcta_tract_rel_10.csv'))
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
    dataset = PopulationDataManager()
    logger.info("Loading Population dataset from 'data' dir")
    dataset.loadAllStateCsvs([
        os.path.join(basedir, 'data', 'ACS_16_5YR_B05006-1', 'ACS_16_5YR_B05006_with_ann.csv'),
        os.path.join(basedir, 'data', 'ACS_16_5YR_B05006-2', 'ACS_16_5YR_B05006_with_ann.csv')
    ])
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
