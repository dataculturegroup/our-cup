<script>
    import { allCounties } from '$lib/counties.js';
    import { page } from '$app/stores';
    import Header from './Header.svelte';
    import Slide from './Slide.svelte';
    import PlacePicker from './placepicker/PlacePicker.svelte';
    import Footer from './Footer.svelte';

    const preselectedFips = $page.url.searchParams.get('fips');
    const preselectedCounty = $derived(allCounties.find(county => county.fips.toString() === preselectedFips));

</script>

<Header />

<main>
    <section id="scrolly">
        <!--
        <Slide image="images/bracket.webp">
            The 2023 Women’s World Cup promises to be the most global tournament yet, with teams from eight nations (🇲🇦🇵🇦🇵🇭🇵🇹🇮🇪🇻🇳🇿🇲) making their debut on this world stage. For many, this is a powerful chance to represent their countries for the first time, inspiring communities back home.
        </Slide>

        <Slide image="images/usa-team-selection.jpg">
            The U.S. team features many players whose families had journeyed to America in search of opportunity, embodying a new era of diversity. Yet, the growing strength of other nations signals that the era of U.S. dominance might be waning -- a positive shift for the global game.
        </Slide>

        <Slide image="images/australia-team.webp">
            Australia and New Zealand, co-hosts of the 2023 Women’s World Cup, bring vibrant cultures and rising soccer ambitions to the global stage. While fans can celebrate the hosts’ passion for sports, the tournament’s distant time zones poses challenges for global audiences who will have to wake up at add hours to watch the games.
        </Slide>

        <Slide image="images/team-flags.jpg">
            Soccer’s global reach has given new nations a chance to shine, with emerging teams challenging traditional powerhouses like the U.S. For immigrant communities, supporting their home or adopted countries became a celebration of resilience and representation.
        </Slide>

        <Slide image="images/serving-fans.jpg">
            Use the button below to find out who your neighbors are supporting. Then get out there and taste their food, listen to their music, support their restaurants, and learn from their home. Celebrate their cultures. Make it Our Cup.
        </Slide>
        -->
    </section>

    <section id="interactive">
        <a name="#interactive" aria-label="try out the interactive"></a>
        <PlacePicker {preselectedCounty} />
    </section>

</main>

<Footer />
