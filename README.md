Games to Watch
==============

A quick web tool that suggests World Cup games to watch in your community based on 
foreign-born populations. This combines US Census data, with a match schedule to suggest
the best games to watch based on the population of people near where you live (or a zip-code
you input),

Dependencies
------------

This is built for Python 3.

```
pip3 install -r requirements.txt
```

Installation
------------

1. Follow the instructions in `data/README.md` to download the latest data you need

2. Run the two scripts in the `scripts` directory:
```
python3 -m scripts.download_fixtures
python3 -m scripts.import_acs_data
```

3. Make sure to create a `cache` directory and make writable by the appropriate user

Data Source for 2018
--------------------

The [Open Football project has published](https://github.com/openfootball/world-cup.json) an easy-to 
use JSON file of the fixtures.  We download and use that from here:

  https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json

Tests
-----

There are a handful of unit tests scattered throughout the modules.  You can run them all by running `python3 test.py`.

Deploying
---------

This is built to deploy to a containerized hosting service like Heroku. The database ends up being too
big to check into GitHub directly (>100MB), so you should make sure there is a predeploy hook to generate the 
database at release time (this can take 5 to 10 minutes).
