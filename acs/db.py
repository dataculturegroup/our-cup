import logging, json
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import distinct

Base = declarative_base()
 
class PopulationInfo(Base):
    __tablename__ = 'population_info'
    id = Column(Integer, primary_key=True)
    tract_id = Column(String(250))
    tract_id2 = Column(String(12))
    label = Column(String(250))
    tract = Column(String(250))
    county = Column(String(250), index=True)
    state = Column(String(250), index=True)
    country = Column(String(250), index=True)
    pop_by_county_json = Column(String(2000))

class ZipCodeInfo(Base):
    __tablename__ = 'zip_code_info'
    id = Column(Integer, primary_key=True)
    zip_code = Column(String(5), index=True)
    state_id = Column(String(2))
    county_id = Column(String(3))
    tract_id = Column(String(6))
    tract_id2 = Column(String(12))

class CensusDataManager():

    def __init__(self,db_connection_str):
        self._logger = logging.getLogger(__name__)
        self._engine = create_engine(db_connection_str)
        self._cache = {}
        Base.metadata.bind = self._engine
        self._createTables()
        self._createSession()

    def _createTables(self):
        Base.metadata.create_all(self._engine)

    def _createSession(self):
        my_session_maker = sessionmaker()
        my_session_maker.bind = self._engine
        self._session = my_session_maker()

    def addPopulationRecord(self,tract_population):
        try:
            new_population_info = PopulationInfo(
                tract_id = tract_population.id,
                tract_id2 = tract_population.id2,
                label = tract_population.label.decode("utf-8"),
                tract = tract_population.tract,
                county = tract_population.county.decode("utf-8"),
                state = tract_population.state,
                country = tract_population.country,
                pop_by_county_json = json.dumps(tract_population.pop_by_country)
            )
            self._session.add(new_population_info)
            self._session.commit()
            return True
        except UnicodeDecodeError:
            #TODO: fix this so it isn't an error case!
            self._logger.error("Unable to decode "+str(tract_population))
            return False

    def addZipCodeRecord(self,tract_zip_code):
        new_zip_code_info = ZipCodeInfo(
            zip_code = tract_zip_code.zip_code,
            state_id = tract_zip_code.state_id,
            county_id = tract_zip_code.county_id,
            tract_id = tract_zip_code.tract_id,
            tract_id2 = tract_zip_code.state_id+tract_zip_code.county_id+tract_zip_code.tract_id
        )
        self._session.add(new_zip_code_info)
        self._session.commit()
        return True

    def emptyZipCodeTable(self):
        self._session.query(ZipCodeInfo).delete()

    def emptyPopulationTable(self):
        self._session.query(PopulationInfo).delete()

    def states(self):
        cache_key = 'states'
        if cache_key in self._cache:
            return self._cache[cache_key]
        self._cache[cache_key] = sorted([l[0] for l in self._session.query(distinct(PopulationInfo.state))])
        return self._cache[cache_key]

    def counties(self,state):
        cache_key = 'counties_in_'+state
        if cache_key in self._cache:
            return self._cache[cache_key] 
        self._cache[cache_key] = sorted([l[0] for l in self._session.query(distinct(PopulationInfo.county)).filter(PopulationInfo.state==state)])
        return self._cache[cache_key]

    def statesWithCounties(self):
        cache_key = 'states_with_countries'
        if cache_key in self._cache:
            return self._cache[cache_key]
        self._cache[cache_key] = {state:self.counties(state) for state in self.states()}
        return self._cache[cache_key]

    def tractId2ToStateCounty(self,tract_id2):
        records = self._session.query(PopulationInfo).filter(PopulationInfo.tract_id2==tract_id2)
        row = records[0]
        return [row.state, row.county]

    def countryPopulationByTractId2List(self,tract_id2_list):
        '''
        '''
        all_records = []
        for tract_id2 in tract_id2_list:
            tract_records = self._session.query(PopulationInfo).filter(PopulationInfo.tract_id2.like(tract_id2[:-1]+'%'))
            [all_records.append(t) for t in tract_records]
        return self._combinePopulations(all_records)

    def countryPopulationByTractId2(self,tract_id2):
        '''
        Aggregate by using information in tract ids - so we end up with about 10 tracts combined.
        Using just one didn't work well.
        '''
        records = self._session.query(PopulationInfo).filter(PopulationInfo.tract_id2.like(tract_id2[:-3]+'%'))
        return self._combinePopulations(records)

    def countryPopulationByCounty(self,state,county):
        '''
        This aggregates across all the tracts in a county, which can be quite a lot of people.
        '''
        cache_key = 'county_pop_'+state+'_'+county
        if cache_key in self._cache:
            return self._cache[cache_key]
        records = self._session.query(PopulationInfo).filter(PopulationInfo.state==state).filter(PopulationInfo.county==county)
        country_to_pop = self._combinePopulations(records)
        self._cache[cache_key] = country_to_pop
        return self._cache[cache_key]

    def tractId2sInZipCode(self,zip_code):
        records = self._session.query(ZipCodeInfo).filter(ZipCodeInfo.zip_code==zip_code)
        return [r.tract_id2 for r in records]

    def _combinePopulations(self, rows):
        country_to_pop = {}
        # prefill stuff
        for alpha2 in json.loads(rows[0].pop_by_county_json):
            country_to_pop[alpha2] = 0
        for row in rows:
            pop_info = json.loads(row.pop_by_county_json)
            for alpha2 in pop_info:
                country_to_pop[alpha2]+=pop_info[alpha2]
        return country_to_pop
