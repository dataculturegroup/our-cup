Our Cup
=======

A quick web tool that suggests World Cup games to watch in your community based on foreign-born 
populations. This combines US Census data, with a match schedule to suggest the best games to 
watch based on the population of people near where you live.

This is created in two parts: a HTML/JSS/CSS scrollytelling site using scrollama.js, and a 
Svelte-based "recommender" that manages the interactive component logic and state.

## Install

1. `cd svelte-recommender`
2. `npm install`

## Developing

1. `cd svelte-recommender`
2. `npm run dev`

## Updating the Data

Updating this to the latest World Cup is a series of automated and manual steps:

1. Open up the notebook at `census-data/data-generation.ipynb` and follow those instructions
2. Copy-and-paste the data in `census-data/country-recs-json` to `svelte-recommender/src/data/recommendations.json`
3. Open up the `census-data/map-generation.ipynb` and run it to generate the new maps; copy them to `svelte-recommender/public/images/map-raw-pop/`
4. Go through each country alpha-3 to generate and save the map to `svelte-recommender/public/images/map-raw-pop/`
5. Update `svelte-recommender/src/data/teams.js` with all the team names and metadata you find
6. Test out the svelte app in `svelte-recommender` (check out the README.md in that dir for more info)
7. Copy the generated JS and CSS files from `svelte-recommender/dist/` to the appropriate directories here
8. Rewrite the narrative in the `index.html` and images configured in `scripts/scrolling.js`
9. Redesign the app's graphic design to match the current tournament a bit
10. Run `npm run build` to build the static files (to `svelte-recommender/dist`). Copy the .js to `scripts/` and the .css to `/styles/`

## Deploying

Once the svelte interactive is built into static JS and CSS, this is ready to deploy to a flat HTML server. I deployed it via GitHub Pages for the free hosting.
