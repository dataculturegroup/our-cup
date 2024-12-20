<script>
    import { allCounties } from '$lib/counties.js';
    import { page } from '$app/stores';
    import Header from './Header.svelte';
    import Slide from './Slide.svelte';
    import PlacePicker from './placepicker/PlacePicker.svelte';
    import Footer from './Footer.svelte';
    import ScrollyStory from './ScrollyStory.svelte';
    import { onMount } from 'svelte';

    // allow bookmarking and sharing a specific county's results
    const preselectedFips = $page.url.searchParams.get('fips');
    const preselectedCounty = $derived(allCounties.find(county => county.fips.toString() === preselectedFips));

</script>

<Header />

<main>
    <ScrollyStory />

    <section style="min-height: 300px;">
        <a name="#interactive" aria-label="try out the interactive"></a>
        <PlacePicker {preselectedCounty} />
    </section>

</main>

<Footer />
