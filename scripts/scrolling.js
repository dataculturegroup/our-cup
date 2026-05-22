
OurCup.scrolling = {

  backdrops: [
    { 'src': 'images/wc-2026-groups.jpg',
      'credit': 'Carlos Barria/Reuters',
      'alt': 'table showing all teh groups Mens 2026 FIFA World Cup',
    },
    { 'src': 'images/ticket-timeline.png',
      'credit': 'Los Angeles World Cup',
      'alt': 'timeline graphic showing the progression of ticket sales for the 2026 FIFA World Cup',
    },
    { 'src': 'images/fifa-peace-prize.jpg',
      'credit': 'White House',
      'alt': 'photo of Infantino presenting the FIFA Peace Prize to President Trump at the White House in Dec 2025',
    },
    { 'src': 'images/philly-fan-fest.jpg',
      'credit': 'Philadelphia Soccer 2026',
      'alt': 'rendered image depicting a large crowd of soccer fans at the Philadelphia Fan Fest for the 2026 FIFA World Cup',
    },
    { 'src': 'images/team-flags.jpg',
      'credit': '',
      'alt': 'grid of flags of competing teams in the 2026 FIFA World Cup',
    },
    { 'src': 'images/brazil-fan.webp',
      'credit': 'AP Photo/Leo Correa',
      'alt': 'a young Brazilian fan wearing a yellow Brazil jersey cheering with his arms raised',
    }
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
