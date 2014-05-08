import logging

from flask import Flask, render_template, request, redirect, url_for

import acs.data, worldcup.fixtures

app = Flask(__name__)

import acs.db, acs.data

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
    return render_template("home.html",
        state = "Massachusetts",
        county = "Middlesex County",
        states_with_counties = db.statesWithCounties()
    )

@app.route("/get-picks",methods=['POST'])
def get_picks():
    logger.info("get picks!")
    state = request.form['state']
    county = request.form[state+'-county']
    return redirect( url_for('recommendations',state=state,county=county) )

@app.route("/picks_for/<state>/<county>")
def recommendations(state,county):
    if state not in db.states():
        flask.abort(400)
    if county not in db.counties(state):
        flask.abort(400)
    pop_map = db.countyPopulationByCountry(state,county)
    games = picker.by_population(pop_map)
    return render_template("picks_for.html",
        state = state,
        county = county,
        states_with_counties = db.statesWithCounties(),
        games = games[:5]
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
