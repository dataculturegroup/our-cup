<script>
    import { onMount } from 'svelte'
    import teams from '$data/teams.json'
    import recommendations from '$data/recommendations.json'
    import fixtures from '$data/fixtures.json'
    import { scrollTo } from './util.js'
    import CountryCard from './CountryCard.svelte'

    onMount( () => {
        scrollTo('recommendations')
    })

    let { county } = $props()

    const countries = $derived.by(() => {
        if (recommendations.hasOwnProperty(county.fips)) {
            return recommendations[county.fips]
        } else {
            return []
        }
    })

    const countryDetails = $derived(countries.map(country => {
        const team = teams[country]
        const teamFixtures = fixtures.filter(fx => fx.homeTeam === country || fx.awayTeam === country)
        return { country, info: team, fixtures: teamFixtures }
    }))
</script>

<style>
#recommendations {
    text-align: center
}
.error {
    margin: 1rem
}
</style>

<div id="recommendations">
    {#if countryDetails.length == 0 }
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

        <div class="container">
            <div class="row">
                {#each countryDetails as { country, info, fixtures }}
                    <CountryCard team={info} {fixtures} {county}/>
                {/each}
            </div>
        </div>

    {/if}
</div>