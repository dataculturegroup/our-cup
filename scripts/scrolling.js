
OurCup.scrolling = {

  backdrops: [
    { 'src': 'images/russia-cup-celebration.jpg',
      'credit': 'Kremlin.ru, CC BY 4.0',
      'alt': 'photo of French national soccer team celebrating their win of the 2018 world up in Russia',
    },
    { 'src': 'images/money-shower-fifa.jpg',
      'credit': 'Philipp Schmidli/Getty Images',
      'alt': 'photo of FIFA head being showered in fake dollar bills by a protester who interrupted a press conference',
    },
    { 'src': 'images/qatar-workers.jpg',
      'credit': 'Kai Pfaffenbach / Reuters',
      'alt': 'photo of migrant workers walking in front of an under construction stadium in Qatar',
    },
    { 'src': 'images/team-flags.jpg',
      'credit': null,
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
