import logging
import json
from flask import render_template, jsonify
import os

from ourcup import app, db
import ourcup.util.geo

logger = logging.getLogger(__name__)


@app.route("/")
def index():
    return render_template("home.html",
                           google_analytics_id=os.getenv('GOOGLE_ANALYICS_ID'),
                           matomo_host=os.getenv('MATOMO_HOST'),
                           matomo_site_id=os.getenv('MATOMO_SITE_ID'))


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
    except Exception as e:
        logger.error("Couldn't get picks for ["+str(zip_code)+"]")
        logger.exception(e)
        return render_template('home-with-error.html',
                               error="Sorry, we couldn't find any information for the zip code "+zip_code+"!")


@app.route("/api/zipcode/<zip_code>.json")
def api_picks_for_zip_code(zip_code):
    try:
        logger.debug("API for Zip: "+zip_code)
        games = _games_for_zip_code(zip_code)
        results = {'status': 'ok', 'location': zip_code, 'results': games}
        return jsonify(results)
    except Exception as e:
        logger.error("Couldn't get api picks for ["+str(zip_code)+"]")
        logger.exception(e)
        return jsonify({
            'status': 'error',
            'location': zip_code,
            'results': [],
            'error': "Sorry, we couldn't find any information for the zip code "+zip_code+"!"
        })


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
    except Exception as e:
        logger.error("Couldn't get picks for ["+str(zip_code)+"]")
        logger.exception(e)
        return render_template('_select-zip-code.html',
                               error="Sorry, we couldn't find any information for the zip code "+zip_code+"!")


@app.route("/l/<lat>/<lng>")
def permalink_picks_for_location(lat, lng):
    try:
        logger.debug("Picks for location: [{},{}]".format(lat, lng))
        [location_description, games] = _games_for_location(lat, lng)
        return render_template('home-with-games.html',
                               games=games,
                               permalink="http://ourcup.info/l/{}/{}".format(round(float(lat), 3), round(float(lng), 3)),
                               intro="Here's the game with the most local fans in your part of "+location_description,
                               scroll_to_results=False)
    except Exception as e:
        logger.error("Couldn't get picks for ["+str(lat)+","+str(lng)+"]")
        logger.exception(e)
        return render_template('home-with-error.html',
                               error="Sorry, we couldn't automatically find your location!")


@app.route("/api/location/<lat>/<lng>.json")
def api_picks_for_location(lat, lng):
    try:
        logger.debug("Picks for location: [{},{}]".format(lat, lng))
        [location_description, games] = _games_for_location(lat, lng)
        results = {'status': 'ok', 'location': location_description, 'results': games}
        return jsonify(results)
    except Exception as e:
        logger.error("Couldn't get api picks for ["+str(lat)+","+str(lng)+"]")
        logger.exception(e)
        return jsonify({
            'status': 'error',
            'location': str(lat)+','+str(lng),
            'results': [],
            'error': "Sorry, we couldn't find any information for that location!"
        })


@app.route("/picks/location/<lat>/<lng>")
def picks_for_location(lat, lng):
    try:
        logger.debug("Picks for location: ["+str(lat)+","+str(lng)+"]")
        [location_description, games] = _games_for_location(lat, lng)
        return render_template('_games.html',
                               games=games,
                               permalink="http://ourcup.info/l/{}/{}".format(round(float(lat), 3), round(float(lng), 3)),
                               intro="Here's the game with the most local fans in your part of "+location_description,
                               scroll_to_results=False)
    except Exception as e:
        # geocoding failed for some reason, so fall back to making user pick location by zip
        logger.error("Couldn't get picks for ["+str(lat)+","+str(lng)+"]")
        logger.exception(e)
        return render_template('_select-zip-code.html',
                               error="Sorry, we couldn't automatically find your location!")


def _games_for_zip_code(zip_code):
    tract_id2s = db.tractId2sInZipCode(zip_code)
    logger.debug("   found "+str(len(tract_id2s))+" tracts: "+" ".join(tract_id2s))
    pop_map = db.countryPopulationByTractId2List(tract_id2s)
    games = ourcup.picker.by_population(pop_map)[:5]
    return games


def _games_for_location(lat, lng):
    place = ourcup.util.geo.reverse_geocode(lat, lng)
    location_description = place['County']['name']+", "+place['State']['code']
    logger.debug("  location details: "+json.dumps(place))
    tract_id2 = place['Block']['FIPS'][:-4]
    pop_map = db.countryPopulationByTractId2(tract_id2)
    games = ourcup.picker.by_population(pop_map)[:5]
    return [location_description, games]
