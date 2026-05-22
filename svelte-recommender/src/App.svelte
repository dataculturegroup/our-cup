<script>
    import { onMount } from 'svelte';
    import allCounties from '$data/counties.json';
    import PlacePicker from './lib/PlacePicker.svelte'

    // load the fips from the URL if it is there, and pass it into the PlacePicker below
    const searchParams = new URLSearchParams(window.location.search);
    const preselectedFips = searchParams.get('fips');
    const preselectedCounty = $derived(allCounties.find(county => county.fips.toString() === preselectedFips));
</script>

<section>
    <PlacePicker preselectedCounty={preselectedCounty}/>
</section>
