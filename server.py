import logging, requests, json, os

from flask import Flask, render_template, request, redirect, url_for, jsonify

import acs.db, acs.data, worldcup.fixtures, util.geo, util.filecache

app = Flask(__name__)

# setup logging
logging.basicConfig(filename='world-cup.log',level=logging.DEBUG)
logger = logging.getLogger('world-cup-server')
logger.info("---------------------------------------------------------------------------")

# connect to database
db = acs.db.CensusDataManager('sqlite:///'+os.path.dirname(os.path.realpath(__file__))+'/acs.db')
logger.info("Connected to db")

picker = worldcup.fixtures.Picker()

# setup cache dir correctly
util.filecache.set_dir(os.path.dirname(os.path.realpath(__file__))+"/cache")

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/z/<zip_code>")
def permalink_picks_for_zip_code(zip_code):
    try:
        logger.debug("Picks for Zip: "+zip_code)
        games = _games_for_zip_code(zip_code)
        return render_template('home-with-games.html', 
            games=games, 
            permalink="http://ourcup.info/z/"+str(zip_code),
            intro="Here's game with the most local fans in "+str(zip_code)+"",
            scroll_to_results=True)
    except:
        logger.error("Couldn't get picks for ["+str(zip_code)+"]")
        logger.exception('')
        return render_template('home-with-error.html',
            error="Sorry, we couldn't find any information for the zip code "+zip_code+"!")

@app.route("/picks/zipcode/<zip_code>")
def picks_for_zip_code(zip_code):
    try:
        logger.debug("Picks for Zip: "+zip_code)
        games = _games_for_zip_code(zip_code)
        return render_template('_games.html', 
            games=games, 
            permalink="http://ourcup.info/z/"+str(zip_code),
            intro="Here's game with the most local fans in "+str(zip_code)+"",
            scroll_to_results=True)
    except:
        logger.error("Couldn't get picks for ["+str(zip_code)+"]")
        logger.exception('')
        return render_template('_select-zip-code.html',
            error="Sorry, we couldn't find any information for the zip code "+zip_code+"!")

@app.route("/l/<lat>/<lng>")
def permalink_picks_for_location(lat,lng):
    try:
        logger.debug("Picks for location: ["+str(lat)+","+str(lng)+"]")
        [location_description,games] = _games_for_location(lat,lng)
        return render_template('home-with-games.html', 
            games=games, 
            permalink="http://ourcup.info/l/"+str(round(float(lat),3))+"/"+str(round(float(lng),3)),
            intro="Here's the game with the most local fans in your part of "+location_description,
            scroll_to_results=False)
    except:
        logger.error("Couldn't get picks for ["+str(lat)+","+str(lng)+"]")
        logger.exception('')
        return render_template('home-with-error.html',
            error="Sorry, we couldn't automatically find your location!")

@app.route("/picks/location/<lat>/<lng>")
def picks_for_location(lat,lng):
    try:
        logger.debug("Picks for location: ["+str(lat)+","+str(lng)+"]")
        [location_description,games] = _games_for_location(lat,lng)
        return render_template('_games.html', 
            games=games, 
            permalink="http://ourcup.info/l/"+str(round(float(lat),3))+"/"+str(round(float(lng),3)),
            intro="Here's the game with the most local fans in your part of "+location_description,
            scroll_to_results=False)
    except:
        # geocoding failed for some reason, so fall back to making user pick location by zip
        logger.error("Couldn't get picks for ["+str(lat)+","+str(lng)+"]")
        logger.exception('')
        return render_template('_select-zip-code.html',
            error="Sorry, we couldn't automatically find your location!")

def _games_for_zip_code(zip_code):
    tract_id2s = db.tractId2sInZipCode(zip_code)
    logger.debug("   found "+str(len(tract_id2s))+" tracts: "+" ".join(tract_id2s))
    pop_map = db.countryPopulationByTractId2List(tract_id2s)
    games = picker.by_population(pop_map)[:5]
    return games

def _games_for_location(lat,lng):
    place = util.geo.reverse_geocode(lat,lng)
    location_description = place['County']['name']+", "+place['State']['code']
    logger.debug("  location details: "+json.dumps(place))
    tract_id2 = place['Block']['FIPS'][:-4]
    pop_map = db.countryPopulationByTractId2(tract_id2)
    games = picker.by_population(pop_map)[:5]
    return [location_description, games]

if __name__ == "__main__":
    app.debug = True
    app.run()
