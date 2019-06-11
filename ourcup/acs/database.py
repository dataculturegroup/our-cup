import logging
import json
from sqlalchemy import distinct
from sqlalchemy.exc import OperationalError
import operator

from ourcup.acs.models import PopulationInfo, ZipCodeInfo


class DatabaseManager:

    def __init__(self, alchemy_db):
        self._logger = logging.getLogger(__name__)
        self._alchemy_db = alchemy_db
        self._cache = {}
        self._createTables()

    def _createTables(self):
        self._logger.info("Creating tables")
        self._alchemy_db.create_all()

    def addPopulationRecord(self, tract_population):
        try:
            new_population_info = PopulationInfo(
                tract_id=tract_population.id,
                tract_id2=tract_population.id2,
                label=tract_population.label,
                tract=tract_population.tract,
                county=tract_population.county,
                state=tract_population.state,
                country=tract_population.country,
                pop_by_county_json=json.dumps(tract_population.pop_by_country)
            )
            self._alchemy_db.session.add(new_population_info)
            self._alchemy_db.session.commit()
            return True
        except UnicodeDecodeError:
            # TODO: fix this so it isn't an error case!
            self._logger.error("Unable to decode "+str(tract_population))
            return False

    def addZipCodeRecord(self, tract_zip_code):
        new_zip_code_info = ZipCodeInfo(
            zip_code=tract_zip_code.zip_code,
            state_id=tract_zip_code.state_id,
            county_id=tract_zip_code.county_id,
            tract_id=tract_zip_code.tract_id,
            tract_id2=tract_zip_code.state_id+tract_zip_code.county_id+tract_zip_code.tract_id
        )
        self._alchemy_db.session.add(new_zip_code_info)
        self._alchemy_db.session.commit()
        return True

    def emptyZipCodeTable(self):
        try:
            self._alchemy_db.session.query(ZipCodeInfo).delete()
        except OperationalError:
            self._logger.warning("Couldn't empty zip code table")

    def emptyPopulationTable(self):
        try:
            self._alchemy_db.session.query(PopulationInfo).delete()
        except OperationalError:
            self._logger.warning("Couldn't empty population data table")

    def states(self):
        cache_key = 'states'
        if cache_key in self._cache:
            return self._cache[cache_key]
        self._cache[cache_key] = sorted([l[0] for l in self._alchemy_db.session.query(distinct(PopulationInfo.state))])
        return self._cache[cache_key]

    def counties(self, state):
        cache_key = 'counties_in_'+state
        if cache_key in self._cache:
            return self._cache[cache_key]
        self._cache[cache_key] = sorted([l[0] for l in self._alchemy_db.session.query(distinct(PopulationInfo.county)).
                                        filter(PopulationInfo.state == state)])
        return self._cache[cache_key]

    def statesWithCounties(self):
        cache_key = 'states_with_countries'
        if cache_key in self._cache:
            return self._cache[cache_key]
        self._cache[cache_key] = {state: self.counties(state) for state in self.states()}
        return self._cache[cache_key]

    def tractId2ToStateCounty(self, tract_id2):
        records = self._alchemy_db.session.\
            query(PopulationInfo).\
            filter(PopulationInfo.tract_id2 == tract_id2)
        row = records[0]
        return [row.state, row.county]

    def countryPopulationByTractId2List(self, tract_id2_list):
        all_records = []
        for tract_id2 in tract_id2_list:
            tract_records = self._alchemy_db.session.\
                query(PopulationInfo).\
                filter(PopulationInfo.tract_id2.like(tract_id2[:-1]+'%'))
            [all_records.append(t) for t in tract_records]
        return DatabaseManager._combinePopulations(all_records)

    def countryPopulationByTractId2(self, tract_id2):
        """
        Aggregate by using information in tract ids - so we end up with about 10 tracts combined.
        Using just one didn't work well.
        """
        records = self._alchemy_db.session.\
            query(PopulationInfo).\
            filter(PopulationInfo.tract_id2.like(tract_id2[:-3]+'%'))
        return DatabaseManager._combinePopulations(records)

    def countryPopulationByCounty(self, state, county):
        """
        This aggregates across all the tracts in a county, which can be quite a lot of people.
        """
        cache_key = 'county_pop_'+state+'_'+county
        if cache_key in self._cache:
            return self._cache[cache_key]
        records = self._alchemy_db.session.\
            query(PopulationInfo).\
            filter(PopulationInfo.state == state).\
            filter(PopulationInfo.county == county)
        country_to_pop = DatabaseManager._combinePopulations(records)
        self._cache[cache_key] = country_to_pop
        return self._cache[cache_key]

    def tractId2sInZipCode(self, zip_code):
        records = self._alchemy_db.session.\
            query(ZipCodeInfo).\
            filter(ZipCodeInfo.zip_code == zip_code)
        return [r.tract_id2 for r in records]

    @staticmethod
    def _combinePopulations(rows):
        country_to_pop = {}
        # pre-fill stuff
        for alpha in json.loads(rows[0].pop_by_county_json):
            country_to_pop[alpha] = 0
        for row in rows:
            pop_info = json.loads(row.pop_by_county_json)
            for alpha in pop_info:
                country_to_pop[alpha] += pop_info[alpha]
        results = [{'country': k, 'population': v} for k, v in country_to_pop.items()]
        results = sorted(results, key=operator.itemgetter('population'), reverse=True)
        return results
