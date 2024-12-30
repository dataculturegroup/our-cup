<script>
    import scrollama from "scrollama";
    import { onMount } from 'svelte';

    const backdrops = [
        { 'src': 'images/bracket.webp',
         'credit': 'World Soccer Talk',
         'alt': 'bracket showing all groups competing in the 2023 world cup',
        },
        { 'src': 'images/usa-team-selection.jpg',
            'credit': 'USSoccer.com',
            'alt': 'photo of players picked for the US national soccer team to compete in the 2023 world cup',
        },
        { 'src': 'images/australia-team.webp',
            'credit': 'Associated Press',
            'alt': 'photo of Australian players celebrating a win',
        },
        { 'src': 'images/team-flags.jpg',
        'credit': 'Amazon',
        'alt': 'digital image of a grid of flags, one for each country in the world cup this year',
        },
        { 'src': 'images/serving-fans.jpg',
        'credit': 'Jane Stockdale',
        'alt': 'photo of soccer fans from different countries watching a game together',
        },
    ];
    
    let scroller;
    onMount(() => {
        scroller = scrollama();
        scroller.setup({
            step: "#scrolly article .step",
            offset: 0.8,
            debug: false
        }).onStepEnter(handleStepEnter)
            .onStepExit(handleStepExit);
    // const main = d3.select("main");
    // const scrolly = main.select("#scrolly");
    // OurCup.scrolling.figure = scrolly.select("#backdrop");
    // const article =scrolly.select("article");
    // OurCup.scrolling.step = article.selectAll(".step");
        handleResize();
        setBackdropImage(0);
    }); 

    function setBackdropImage(index) {
        const img = backdrops[index];
        const backdropImg = document.getElementById("backdrop-img");
        backdropImg.setAttribute('src', img.src);
        backdropImg.setAttribute('alt', img.alt);
        document.getElementById("backdrop-caption").innerHTML = img.credit;
    }
    
    function handleStepEnter(stepInfo) { // stepInfo = { element, directihandle, index }
        // chandlesole.log(stepInfo);
        //OurCup.scrolling.step.classed("is-active", (d, i) => i === stepInfo.index);
        setBackdropImage(stepInfo.index);
    }

    function handleStepExit(stepInfo){
        return null;
    }

    function handleResize() {
        const stepH = Math.floor(window.innerHeight * 1); // update step heights
        document.querySelectorAll('.step').forEach(step => {
            step.style.height = `${stepH}px`;
        });
        const figureHeight = window.innerHeight;
        const figureMarginTop = 0;
        const backdrop = document.getElementById("backdrop");
        backdrop.style.height = figureHeight + "px";
        backdrop.style.top = figureMarginTop + "px";
        const backdropWrapper = document.getElementById("background-wrapper");
        backdropWrapper.height = figureHeight + "px";
        scroller.resize(); // tell scrollama to update new element dimensihandles
    }
</script>
<style>

#scrolly {
	position: relative;
}

article {
	position: relative;
	padding: 0;
	max-width: 50rem;
	margin: 0 auto;
}

figure {
	position: -webkit-sticky;
	position: sticky;
	left: 0;
	width: 100%;
  height: 100%;
	margin: 0;
	-webkit-transform: translate3d(0, 0, 0);
	-moz-transform: translate3d(0, 0, 0);
	transform: translate3d(0, 0, 0);
	z-index: 0;
  background-color: #333;
}

figure div.wrapper {
  display: flex;
  justify-content: center;
}

figure img {
  height: 100%;
}

figure {
  overflow: hidden;
}

figure p {
	text-align: center;
	padding: 1rem;
	position: absolute;
	top: 50%;
	left: 50%;
	-moz-transform: translate(-50%, -50%);
	-webkit-transform: translate(-50%, -50%);
	transform: translate(-50%, -50%);
	font-size: 8rem;
	font-weight: 900;
	color: #fff;
}

#backdrop-caption {
  position: relative;
  top: -2.5rem;
  color: #000;
  background-color: white;
  display: inline-block;
  font-size: 0.75rem;
  padding: 0 0.5rem;
  opacity: 0.4;
}

.step {
  filter: drop-shadow(0px 0px 8px #000);
}

.step:last-child {
	margin-bottom: 0;
}

.step.is-active p {
}

.step p {
  border-radius: 0.5rem;
  text-align: center;
	padding: 1rem;
	font-size: 1.5rem;
	background-color: #fff;
  margin: 0 2rem;
}
</style>
<section id="scrolly">

    <figure id="backdrop">
        <div class="wrapper" id="background-wrapper">
                <img id="backdrop-img" alt="(will be replaced by code)"/>
        </div>
        <div id="backdrop-caption"></div>
            </figure>

            <article>
                <div class="step" data-step="1">
                    <p>
            The 2023 Women’s World Cup promises to be the most global tournament yet, 
            with teams from eight nations (🇲🇦🇵🇦🇵🇭🇵🇹🇮🇪🇻🇳🇿🇲) making their debut on this world
            stage. For many, this is a powerful chance to represent their 
            countries for the first time, inspiring communities back home.
        </p>
                </div>
                <div class="step" data-step="2">
                    <p>
            The U.S. team features many players whose families had journeyed to America in
            search of opportunity, embodying a new era of diversity. Yet, the growing
            strength of other nations signals that the era of U.S. dominance might be
            waning -- a positive shift for the global game.
        </p>
                </div>
                <div class="step" data-step="3">
                    <p>
            Australia and New Zealand, co-hosts of the 2023 Women’s World Cup, bring
            vibrant cultures and rising soccer ambitions to the global stage. While 
            fans can celebrate the hosts’ passion for sports, the tournament’s distant 
            time zones poses challenges for global audiences who will have to wake up
            at add hours to watch the games.
        </p>
                </div>
                <div class="step" data-step="4">
                    <p>
            Soccer’s global reach has given new nations a chance to shine, with 
            emerging teams challenging traditional powerhouses like the U.S. 
            For immigrant communities, supporting their home or adopted countries 
            became a celebration of resilience and representation.
        </p>
                </div>
        <div class="step" data-step="4">
                    <p>
            Use the button below to find out who your neighbors are supporting.
            Then get out there and taste their food, listen to their music, support their restaurants, 
            and learn from their home. Celebrate their cultures.
            Make it <em>Our Cup</em>.
        </p>
                </div>
            </article>
</section>
