import logging, json
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import distinct

Base = declarative_base()
 
class CensusTract(Base):
    __tablename__ = 'census_tract'
    id = Column(Integer, primary_key=True)
    tract_id = Column(String(250))
    tract_id2 = Column(String(250))
    label = Column(String(250))
    tract = Column(String(250))
    county = Column(String(250), index=True)
    state = Column(String(250), index=True)
    country = Column(String(250), index=True)
    pop_by_county_json = Column(String(2000))

class CensusDataManager():

    def __init__(self,db_connection_str):
        self._logger = logging.getLogger(__name__)
        self._engine = create_engine(db_connection_str)
        Base.metadata.bind = self._engine
        self._createTables()
        self._createSession()

    def _createTables(self):
        Base.metadata.create_all(self._engine)

    def _createSession(self):
        my_session_maker = sessionmaker()
        my_session_maker.bind = self._engine
        self._session = my_session_maker()

    def addRecord(self,census_tract_record):
        try:
            new_census_tract = CensusTract(
                tract_id = census_tract_record.id,
                tract_id2 = census_tract_record.id2,
                label = census_tract_record.label.decode("utf-8"),
                tract = census_tract_record.tract,
                county = census_tract_record.county.decode("utf-8"),
                state = census_tract_record.state,
                country = census_tract_record.country,
                pop_by_county_json = json.dumps(census_tract_record.pop_by_country)
            )
            self._session.add(new_census_tract)
            self._session.commit()
            return True
        except UnicodeDecodeError:
            self._logger.error("Unable to decode "+str(census_tract_record))
            return False

    def empty(self):
        self._session.query(CensusTract).delete()

    def states(self):
        return sorted([l[0] for l in self._session.query(distinct(CensusTract.state))])

    def counties(self,state):
        return sorted([l[0] for l in self._session.query(distinct(CensusTract.county)).filter(CensusTract.state==state)])

    def statesWithCounties(self):
        return {state:self.counties(state) for state in self.states()}

    def countyPopulationByCountry(self,state,county):
        records = self._session.query(CensusTract).filter(CensusTract.state==state).filter(CensusTract.county==county)
        country_to_pop = {}
        # prefill stuff
        for alpha2 in json.loads(records[0].pop_by_county_json):
            country_to_pop[alpha2] = 0
        # now aggregate
        for record in records:
            pop_info = json.loads(record.pop_by_county_json)
            for alpha2 in pop_info:
                country_to_pop[alpha2]+=pop_info[alpha2]
        return country_to_pop
