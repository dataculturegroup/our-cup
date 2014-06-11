import logging, requests, json

from flask import Flask, render_template, request, redirect, url_for, jsonify

import acs.db, acs.data, worldcup.fixtures, util.geo

app = Flask(__name__)

# setup logging
logging.basicConfig(filename='world-cup.log',level=logging.DEBUG)
logger = logging.getLogger('world-cup-server')
logger.info("---------------------------------------------------------------------------")

# connect to database
db = acs.db.CensusDataManager('sqlite:///acs.db')
logger.info("Connected to db")

picker = worldcup.fixtures.Picker()

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/picks/zipcode/<zip_code>")
def picks_for_zip_code(zip_code):
    tract_id2s = db.tractId2sInZipCode(zip_code)
    pop_map = db.countryPopulationByTractId2List(tract_id2s)
    tract_games = picker.by_population(pop_map)[:5]
    return jsonify({'zipcode_games':tract_games})

@app.route("/picks/location/<lat>/<lng>")
def picks_for_location(lat,lng):
    try:
        place = util.geo.reverse_geocode(lat,lng)
        tract_id2 = place['Block']['FIPS'][:-4]
        pop_map = db.countryPopulationByTractId2(tract_id2)
        tract_games = picker.by_population(pop_map)[:5]
        return jsonify({'tract_list_games':tract_games})
    except:
        # geocoding failed for some reason, so fall back to making user pick location
        # TODO
        return jsonify({'error':1})

if __name__ == "__main__":
    app.debug = True
    app.run()
