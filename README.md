Our Cup
=======

A quick web tool that suggests World Cup games to watch in your community based on
foreign-born populations. This combines US Census data, with a match schedule to suggest
the best games to watch based on the population of people near where you live.

Updating
--------

Updating this to the latest World Cup is a series of automated and manual steps:

1. Open up the notebook at `census-data/data-generation.pynb` and follow those instructions
2. Copy-and-paste the data in `census-data/country-recs-json` to `data/recommendations.json`
3. Open the [county-map observable notebook](https://observablehq.com/d/62390c8bd663ff6f) and update the `county-populaton-data-tidy.csv` file
4. Go through each country alpha-3 to generate and save the map to `images/map-raw-pop`
5. Update `data/teams.js` with all the team names and metadata you find
6. Now you're ready to write the story and build the interactive you want to

Deploying
---------

This is built to deploy to a flat HTML server. I deployed it via GitHub Pages for
the free hosting.
