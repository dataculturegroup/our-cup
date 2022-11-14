
OurCupScrolling = {

  backdrops: [
    { 'src': 'images/russia-cup-celebration.jpg',
      'credit': 'Kremlin.ru, CC BY 4.0',
    },
    { 'src': 'images/money-shower-fifa.jpg',
      'credit': 'Philipp Schmidli/Getty Images'
    },
    { 'src': 'images/qatar-workers.jpg',
      'credit': 'Kai Pfaffenbach / Reuters'
    },
    { 'src': 'images/team-flags.jpg',
      'credit': null
    },
    { 'src': 'images/serving-fans.jpg',
      'credit': 'Jane Stockdale'
    },
  ],

  initialize: function() {
    OurCupScrolling.scroller = scrollama();
    var main = d3.select("main");
    var scrolly = main.select("#scrolly");
    OurCupScrolling.figure = scrolly.select("#backdrop");
    var article =scrolly.select("article");
    OurCupScrolling.step = article.selectAll(".step");
    OurCupScrolling.handleResize();
    OurCupScrolling.setBackdropImage(0);
    OurCupScrolling.scroller
      .setup({
        step: "#scrolly article .step",
        offset: 0.8,
        debug: false
      })
      .onStepEnter(OurCupScrolling.handleStepEnter)
      .onStepExit(OurCupScrolling.handleStepExit);
  },

  setBackdropImage: function(index) {
    OurCupScrolling.figure.select("img")
      .attr('src', OurCupScrolling.backdrops[index].src)
      .attr('class', 'fade-in');
  },

  handleStepEnter: function(stepInfo) { // stepInfo = { element, directihandle, index }
    // chandlesole.log(stepInfo);
    OurCupScrolling.step.classed("is-active", function (d, i) {  // highlight current step
      return i === stepInfo.index;
    });
    OurCupScrolling.setBackdropImage(stepInfo.index)
  },

  handleStepExit: function(stepInfo) {
  },

  handleResize: function() {
    var stepH = Math.floor(window.innerHeight * 1); // update step heights
    OurCupScrolling.step.style("height", stepH + "px");
    var figureHeight = window.innerHeight;
    var figureMarginTop = 0;
    OurCupScrolling.figure
      .style("height", figureHeight + "px")
      .style("top", figureMarginTop + "px");
    OurCupScrolling.figure.select(".wrapper")
      .style("height", figureHeight + "px")
    OurCupScrolling.scroller.resize(); // tell scrollama to update new element dimensihandles
  }

};
