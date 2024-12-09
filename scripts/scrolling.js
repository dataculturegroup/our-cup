
OurCup.scrolling = {

  backdrops: [
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
  ],

  initialize: () => {
    OurCup.scrolling.scroller = scrollama();
    const main = d3.select("main");
    const scrolly = main.select("#scrolly");
    OurCup.scrolling.figure = scrolly.select("#backdrop");
    const article =scrolly.select("article");
    OurCup.scrolling.step = article.selectAll(".step");
    OurCup.scrolling.handleResize();
    OurCup.scrolling.setBackdropImage(0);
    OurCup.scrolling.scroller
      .setup({
        step: "#scrolly article .step",
        offset: 0.8,
        debug: false
      })
      .onStepEnter(OurCup.scrolling.handleStepEnter)
      .onStepExit(OurCup.scrolling.handleStepExit);
  },

  setBackdropImage: (index) => {
    const img = OurCup.scrolling.backdrops[index]
    OurCup.scrolling.figure.select("img")
      .attr('src', img.src)
      .attr('alt', img.alt)
      .attr('class', 'fade-in');
    d3.select("#backdrop-caption").html(img.credit)
  },

  handleStepEnter: (stepInfo) => { // stepInfo = { element, directihandle, index }
    // chandlesole.log(stepInfo);
    OurCup.scrolling.step.classed("is-active", (d, i) => i === stepInfo.index);
    OurCup.scrolling.setBackdropImage(stepInfo.index)
  },

  handleStepExit: (stepInfo) => {
  },

  handleResize: () => {
    const stepH = Math.floor(window.innerHeight * 1); // update step heights
    OurCup.scrolling.step.style("height", stepH + "px");
    const figureHeight = window.innerHeight;
    const figureMarginTop = 0;
    OurCup.scrolling.figure
      .style("height", figureHeight + "px")
      .style("top", figureMarginTop + "px");
    OurCup.scrolling.figure.select(".wrapper")
      .style("height", figureHeight + "px")
    OurCup.scrolling.scroller.resize(); // tell scrollama to update new element dimensihandles
  }

};
