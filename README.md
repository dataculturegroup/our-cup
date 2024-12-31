Our Cup
=======

A quick web tool that suggests World Cup games to watch in your community based on foreign-born populations. This combines US Census data, with a match schedule to suggest the best games to watch based on the population of people near where you live.

This is created in two parts: a HTML/JSS/CSS scrollytelling site using scrollama.js, and a  Svelte-based "recommender" that manages the interactive component logic and state.

Updating
--------

Updating this to the latest World Cup is a series of automated and manual steps:

1. Open up the notebook at `census-data/data-generation.pynb` and follow those instructions
2. Copy-and-paste the data in `census-data/country-recs-json` to `svelte-recommender/src/data/recommendations.json`
3. Open the [county-map observable notebook](https://observablehq.com/d/62390c8bd663ff6f) and update the `county-populaton-data-tidy.csv` file
4. Go through each country alpha-3 to generate and save the map to `images/map-raw-pop` and `svelte-recommender/public/images/map-raw-pop/`
5. Update `svelte-recommender/src/data/teams.js` with all the team names and metadata you find
6. Test out the svelte app in `svelte-recommender` (check out the README.md in that dir for more info)
7. Copy the generated JS and CSS files from `svelte-recommender/dist/` to the appropriate directories here
8. Now you're ready to update the story

Deploying
---------

Once the svelte interactive is built into static JS and CSS, this is ready to deploy to a flat HTML server. I deployed it via GitHub Pages for the free hosting.
