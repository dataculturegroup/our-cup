<!--
Card with details about a country's local cultural connection and games to watch.
-->
<script>
    import teams from '$data/teams.json';   // static file with desk research on country
    let { team, fixtures, county } = $props();  // parent passes in all the info we need to show

    // state: toggles whether to show the immigration chloropleth map or not
    let showMap = $state(false);

    // state mgmt: clean up and localize game data by looking up the selected country in pre-computed fixtures data
    const games = $derived(fixtures.map(fx => {
        const homeTeam = teams[fx.homeTeam];
        const awayTeam = teams[fx.awayTeam];
        const localDate = new Date(fx.dateUTC);
        return { homeTeam, awayTeam, localDate };
    }))
</script>

<style>
.team-card {
    margin-top: 2rem;
    padding: 1rem;
    border: 2px solid #471705;
    border-radius: 0.25rem;
    text-align: left;
}
h3 {
    font-family: "Gill Sans", sans-serif;
    margin-top: 1rem;
    font-variant: all-small-caps;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
}
.flag {
    font-size: 120px;
    display: block;
    margin-top: -30px;
    margin-bottom: -30px;
    text-align: center;
}
.team-card ul {
    list-style-type: none;
    margin: 0;
    margin-left: .25rem;
    padding: 0;
}
.team-card ul li {
    margin-bottom: .25rem;
    font-size: 1.25rem;
}
.team-card p {
    font-size: 1.25rem;
}
</style>

<!-- render as 1/3 of full width (12 columns) -->
<div class="col-md-4" id="team-card-{team.alpha3}">
    <div class="team-card">
        <h3>{team.name}</h3>
        <span class="flag">{team.flag}</span>

        <!-- links to local cultural connections -->
        <p>
            🍲 Support a local business - find a <a target="_blank" href="https://www.yelp.com/search?find_desc={team.name} {team.foodSearch || ''}&find_loc={county.name} {county.state}">{team.demonym} restaurant near you on Yelp</a>, 
            or make <a target="_blank" href="https://www.yummly.com/recipes?q={team.name} {team.foodSearch || ''}">a {team.demonym} recipe from Yummly</a>.
            📖 Learn about <a target="_blank" href="{team.wikipediaUrl}">{team.name} on Wikipedia</a>, 
            or read from some local journalists on <a target="_blank" href="{team.globalVoicesUrl}">Global Voices {team.name}</a>. 
            🎵 Use Spotify to listen to <a target="_blank" href="{team.spotify[0].url}">{team.spotify[0].name}</a>,
                or <a target="_blank" href="{team.spotify[1].url}">{team.spotify[1].name}</a>. 
            {#if team.teamGuide}
                ⚽️ Read the <a target="_blank" href="{team.teamGuide}">{team.demonym} team guide on the Guardian</a>. 
            {/if}
            See a <a href="#immigrant-map" onclick={() => showMap = !showMap}>map of where {team.demonym} immigrants live across the US</a>.
        </p>

        <!-- toggle-able map from Observable notebok -->
        {#if showMap}
            <p>
                <b>Map of {team.demonym} immigrants</b>
                <img width="100%" src="images/map-raw-pop/{team.alpha3}.png"
                    alt="map of US counties showing where the most {team.demonym} immigrants live">
            </p>
        {/if}

        <!-- games to watch -->
        <p><b>Games to watch:</b></p>
        <ul>
            {#each games as {homeTeam, awayTeam, localDate}}
                <li>
                    {localDate.toLocaleDateString()}:
                    {homeTeam.flag} {homeTeam.name}
                    vs
                    {awayTeam.flag} {awayTeam.name}
                </li>
            {/each}
        </ul>

    </div>
</div>