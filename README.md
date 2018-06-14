Games to Watch
==============

A quick web tool that suggests World Cup games to watch in your community based on 
foreign-born populations.

Dependencies
------------

```
pip install -r requirements.txt
```

Installation
------------

1. Follow the instructions in `data/README.md` to download the latest data you need

2. Run the two scripts in the `scripts` directory:
```
python -m scripts.download_fixtures
python -m scripts.import_acs_data
```

3. Make sure to create a `cache` directory and make writable by your web user

Fixtures Data Source for 2018
-----------------------------

The [Open Football project has published](https://github.com/openfootball/world-cup.json) an easy-to 
use JSON file of the fixtures.  We download and use that from here:

  https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json
