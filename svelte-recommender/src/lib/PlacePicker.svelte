<!--
The top-level component that runs the whole interactive. This manages:
 * setting any default state
 * conditionally showing child components
 * showing feedback status
 * auto-detecting a user's location via the brower's geolocation API
 * updating the browser URL
-->
<script>
    import allCounties from '$data/counties.json'; // generated from the Observable notebook mentioned in the README
    import { delay, scrollTo } from './util.js'; 
    import StateOptions from './StateOptions.svelte'; // a simple Svelte component that lists all US states as select item options
    import Recommendations from './Recommendations.svelte'; // a component that shows a list of teams and their games

    // if the parent has specified a county to start on, respect that
    let { preselectedCounty } = $props();

    // Svelte manages these variables (via the `$state` call) so that any changes force the UI to update
    let selectedMode = $state(preselectedCounty ? 'manual' : 'automatic');
    let selectedStateAbbr = $state(preselectedCounty ? preselectedCounty.state : null);
    let selectedCountyFips = $state(preselectedCounty ? preselectedCounty.fips : null);
    let clickedGo = $state(preselectedCounty ? true : false);
    let geolocationSupported = navigator.geolocation ? true : false;
    // find the counties in the US state the user picked, from the static list
    // (Svelte will update this automatically via `$derived` when `selectedStateAbbr` changes)
    const filteredCounties = $derived(allCounties.filter(county => county.state === selectedStateAbbr));
    // find the county object from the static list of all the counties
    // (Svelte will update this automatically via `$derived` when `selectedCountyFips` changes)
    const selectedCounty = $derived(allCounties.find(county => county.fips === selectedCountyFips));

    // event handler: set the mode to manual when the user clicks "manually pick"
    function handleManual() {
        selectedMode = 'manual';
        disableButtons();
        enableButtons();
    }

    // event handler: use the browser's geolocation API to find the user's location when user clicks "automatically detect" 
    function handleAutomatic() {
        disableButtons();
        selectedMode = 'automatic';
        showStatus("Detecting your location...");
        navigator.geolocation.getCurrentPosition(handleLocateSuccess, handleLocateError);
        // don't need to enableButtons here since the geolocation handler will do it for you
    }

    // event handler: when the browser's geolocation API successfully finds the user's location we need to
    // set the FIPS code for the county they are in (via openGov FCC API)
    function handleLocateSuccess(position) {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        showStatus("Zooming to county...");
        const fccApiUrl = `https://geo.fcc.gov/api/census/area?lat=${lat}&lon=${lng}&censusYear=2020&format=json`;
        fetch(fccApiUrl)
            .then((response) => response.json())
            .then((data) => {
                console.log(data.results[0])
                selectedCountyFips = data.results[0].county_fips // this will automatically update selectedCounty
                handleGo()
            });
    }

    // event handler: when the browser's geolocation API fails to find the user's location show a reasonable error msg
    function handleLocateError(error) {
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

    // helper functions to grey out the buttons while things are happening
    function disableButtons() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => button.disabled = true);
    }
    function enableButtons() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => button.disabled = false);
    }
    
    // helper function to update the URL with the selected county FIPS code, using teh Breowser's History API
    function setSearchParam(paramName, paramValue) {
        const url = new URL(window.location.href);      // Get the current URL
        url.searchParams.set(paramName, paramValue);
        history.pushState({}, '', url);                 // Update the URL without reloading
    }

    // helper function to animate through a series of artificial status messages when user hits "go"
    function handleGo() {
        // save state on URL before rendering
        const url = new URL(window.location);
        setSearchParam('fips', selectedCountyFips);
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
            clickedGo = true;
            return delay(500);
        });
    }

    // helper functions to show and hide the status message
    function showStatus(msg) {
        document.getElementById('status').style.display = 'block';
        document.getElementById("statusMsg").innerHTML = msg;
    }
    function hideStatus() {
        document.getElementById('status').style.display = 'none';
        document.getElementById("statusMsg").innerHTML = '';
    }

    // event handler: when the user changes the state, reset things so recommendations don't show
    const handleLocChange = () => clickedGo = false;
</script>

<style>
#interactive {
    text-align: center;
    margin-top: 2rem;
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
        <div id="status" style="display: none">
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