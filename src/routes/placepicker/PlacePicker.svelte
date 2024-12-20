<script>
    import { allCounties } from '$lib/counties.js';
    import { delay, scrollTo } from '$lib/util.js';
    import StateOptions from './StateOptions.svelte';
    import Recommendations from '../recommendations/Recommendations.svelte';

    let { preselectedCounty } = $props();

    let selectedMode = $state(preselectedCounty ? 'manual' : 'automatic');
    let selectedStateAbbr = $state(preselectedCounty ? preselectedCounty.state : null);
    let selectedCountyFips = $state(preselectedCounty ? preselectedCounty.fips : null);
    let clickedGo = $state(preselectedCounty ? true : false);
    let geolocationSupported = navigator.geolocation ? true : false;

    const filteredCounties = $derived(
        allCounties.filter(county => county.state === selectedStateAbbr)
    );

    const selectedCounty = $derived(
        allCounties.find(county => county.fips === selectedCountyFips)
    );

    function handleManual() {
        selectedMode = 'manual';
        disableButtons();
        enableButtons();
    }

    function handleAutomatic() {
        disableButtons();
        selectedMode = 'automatic';
        showStatus("Detecting your location...")
        navigator.geolocation.getCurrentPosition(handleLocateSuccess, handleLocateError);
        //enableButtons();
    }

    function handleLocateSuccess(position) {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        showStatus("Zooming to county...");
        const fccApiUrl = `https://geo.fcc.gov/api/census/area?lat=${lat}&lon=${lng}&censusYear=2020&format=json`;
        fetch(fccApiUrl)
            .then((response) => response.json())
            .then((data) => {
                console.log(data.results[0]);
                selectedCountyFips = data.results[0].county_fips;
                handleGo();        // to update the URL
                location.reload(); // hack to run page code cleanly
            });
    }

    function handleLocateError(error) {
        console.log(error.code);
        let errorMsg = '';
        switch(error.code) {
            case "unsupported":
                errorMsg = "Browser doesn't support Geolocation.";
                break;
            case error.PERMISSION_DENIED:
                errorMsg = "User denied the request for Geolocation.";
                break;
            case error.POSITION_UNAVAILABLE:
                errorMsg = "location information is unavailable.";
                break;
            case error.TIMEOUT:
                errorMsg = "The request to get user location timed out.";
                break;
            case error.UNKNOWN_ERROR:
                errorMsg = "An unknown error occurred.";
                break;
        }
        hideStatus();
        enableButtons();
    }

    function disableButtons() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => button.disabled = true);
    }

    function enableButtons() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => button.disabled = false);
    }
    
    function handleGo() {
        // show user feedback so they understand what went into this
        delay(1).then(() => {
            scrollTo('status');
            showStatus("Gathering census data...");
            return delay(1000);
        }).then(() => {
            showStatus("Doing some math...");
            return delay(1000);
        }).then(() => {
            showStatus("Calculating top teams...");
            return delay(1000);
        }).then(() => {
            showStatus("Finding games...");
            return delay(1000);
        }).then(() => {            
            hideStatus();
            // save state on URL before rendering
            const url = new URL(window.location);
            url.searchParams.set('fips', selectedCountyFips);
            window.history.pushState({}, '', url);
            clickedGo = true;
            return delay(500);
        });
    }

    function showStatus(msg) {
        document.getElementById('status').style.display = 'block';
        document.getElementById("statusMsg").innerHTML = msg;
    }

    function hideStatus(msg) {
        document.getElementById('status').style.display = 'none';
        document.getElementById("statusMsg").innerHTML = '';
    }

    const handleLocChange = () => clickedGo = false;
</script>

<style>
#interactive {
    text-align: center;
}
button {
    margin-top: 1rem;
}
button:disabled {
    opacity: 0.5;
}
#status {
    margin-top: 1rem;
}
</style>

<div class="container" id="interactive">
    <div class="col-md-6 offset-md-3">

        <h2>Where do you live?</h2>
        <p>Find out which fans live near you and get links to their food, music, news, and when their teams are playing.</p>
        <p>
            <button class="btn btn-primary btn-lg" disabled={!geolocationSupported} onclick={handleAutomatic}>
                Locate Me Now
                {#if !geolocationSupported}
                    (not supported)
                {/if}
            </button>
            or
            <button class="btn btn-outline-primary btn-lg" onclick={handleManual}>Manually Pick</button>
        </p>

        {#if selectedMode === 'manual'}
            <div id="manual-selection">
                <label for="state">Select your location:</label>
                <select id="state" name="state" bind:value={selectedStateAbbr} onchange={handleLocChange} class="form-select">
                    <StateOptions />
                </select>
                <select id="county" name="county" bind:value={selectedCountyFips} onchange={handleLocChange} class="form-select">
                    {#each filteredCounties as county}
                        <option value={county.fips}>{county.name}</option>
                    {/each}
                </select>
                <button class="btn btn-primary btn-lg" onclick={handleGo}
                        disabled={selectedStateAbbr === null || selectedCountyFips === null}>
                    Go
                </button>
            </div>
        {/if}
        <div id="status" style="display: none;">
            <div class="spinner-border" role="status"></div>
            <div id="statusMsg"></div>
        </div>
    </div>
</div>

<div id="recommendationsWrapper">
    {#if clickedGo && selectedCounty }
        <Recommendations county={selectedCounty} />
    {/if}
</div>
