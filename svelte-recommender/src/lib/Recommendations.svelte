<!--
Wrapper that shows recommended 3 teams to follow based on the user's selections. This handles:
 * finding the top 3 teams and fixtures for the user's county based on precomputed data from the census analysis in the jupyter notebook
 * rendering a CountryCard for each
-->
<script>
    import { onMount } from 'svelte';   // event handler registration called automatically when the component is visible on page
    import teams from '$data/teams.json'; // static manually curated data about participants in World Cup
    import recommendations from '$data/recommendations.json'; // computed data from Python notebook based on census data
    import fixtures from '$data/fixtures.json'; // static data downloaded from soccer website
    import { scrollTo } from './util.js';   // utility function to scroll to a specific element
    import CountryCard from './CountryCard.svelte'; // a component that shows a single team and its games

    onMount( () => {
        // need to do this in `onMount` handler called automatically by Svelte because we have to make sure the
        // component is fully rendered before we can scroll to it (can't scroll to something we can't see!)
        scrollTo('recommendations');
    })

    // the parent pases in the county the user selected 
    let { county } = $props();

    // state mgmt: figure out countires by looking up the selected county fips in pre-computed recommendations data
    const countries = $derived.by(() => { // using `$derived.by` here so I can use a function
        if (recommendations.hasOwnProperty(county.fips)) {
            return recommendations[county.fips];
        } else {
            return [];  // be safe and handle missing data by showing nothing at all
        }
    })

    // state mgmt: pick the country info I wrote and the fixtures, based on selected county
    const countryDetails = $derived(countries.map(country => {
        const team = teams[country];
        // need to check for games the team is either home or away in
        const teamFixtures = fixtures.filter(fx => fx.homeTeam === country || fx.awayTeam === country);
        return { country, info: team, fixtures: teamFixtures };
    }))
</script>

<style>
#recommendations {
    text-align: center;
}
.error {
    margin: 1rem;
}
</style>

<div id="recommendations">
    {#if countryDetails.length == 0 }
        <!-- show an error if recommendations aren't found -->
        <div class="container">
            <div class="row">
                <div class="col-md-6 offset-md-3">
                    <div class="error alert alert-warning" role="alert">
                        <h2>⚠️ Error</h2>
                        <p>Can't find any recommendations for {county.name}, {county.state} (fips={county.fips}).</p>
                    </div>
                </div>
            </div>
        </div>
    {:else }
        <!-- intro paragraph summarizing top teams -->
        <div class="container">
            <div class="row">
                <div class="col-md-6 offset-md-3">
                    <h2>Top Teams for {county.name}, {county.state}</h2>
                    <p>
                        Many of your neighbors are from 
                        {countryDetails[0].info.flag} {countryDetails[0].info.name},
                        {countryDetails[1].info.flag} {countryDetails[1].info.name}, and
                        {countryDetails[2].info.flag} {countryDetails[2].info.name}.
                    </p>
                </div>
            </div>
        </div>
        <!-- render on CountryCard for each top country, based on immigrant popualtions in selected county -->
        <div class="container">
            <div class="row"> <!-- each card will be rendered as 4 columns -->
                {#each countryDetails as { country, info, fixtures }}
                    <CountryCard team={info} {fixtures} {county}/>
                {/each}
            </div>
        </div>
    {/if}
</div>