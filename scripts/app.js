
OurCup.app = {

  initialize: () => {
    OurCup.app.updateCounties('AL');
    const url = new URL(window.location);
    const preloadFips = url.searchParams.get('fips');
    if(preloadFips){
      const matchedCounty = OurCup.data.counties.filter(c => c.fips == preloadFips);
      if(matchedCounty.length == 1) {
        OurCup.app.updateResultsFromCounty(matchedCounty[0].fips.toString(), matchedCounty[0].name, matchedCounty[0].state)
      }
    }
  },

  handleAutodetect: () => {
    d3.selectAll('#interactive button').property('disabled', true);
    d3.select('#recsWrapper').style('display', 'none');
    OurCup.app.updateStatus(true, "Detecting your location...");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(OurCup.app.handleGeoLocateSuccess, OurCup.app.handleGeoLocateError);
    } else {
        OurCup.app.onGeoLocateError("unsupported");
    }
  },

  handleGeoLocateSuccess: (position) => {
    OurCup.app.updateResultsFromLatLng(position.coords.latitude, position.coords.longitude);
  },

  handleGeoLocateError: (error) => {
    d3.selectAll('#interactive button').property('disabled', false);
    OurCup.app.updateStatus(true, "Couldn't detect your location - sorry!");
    switch(error.code) {
        case "unsupported":
            OurCup.log("Browser doesn't support GeoLocation.");
            break;
        case error.PERMISSION_DENIED:
            OurCup.log("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            OurCup.log("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            OurCup.log("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            OurCup.log("An unknown error occurred.");
            break;
    }
  },

  updateResultsFromLatLng: (lat,lng) => {
    fetch("https://geo.fcc.gov/api/census/area?lat="+lat+"&lon="+lng+"&censusYear=2020&format=json")
      .then((response) => response.json())
      .then((data) => OurCup.app.updateResultsFromCounty(data.results[0].county_fips,
                                                         data.results[0].county_name,
                                                         data.results[0].state_code));
  },

  updateCounties: (state) => {
    var stateCounties = OurCup.data.counties.filter(c => c.state == state);
    var options = stateCounties.map(c => "<option value=\""+c.fips+"\">"+c.name+"</option>")
    d3.select('#county-select').html(options);
  },

  updateUrl: (fips) => {
    const url = new URL(window.location);
    url.searchParams.set('fips', fips);
    window.history.pushState({}, '', url);
  },

  updateResultsFromCounty: (fips, countyName, stateCode) => {
    OurCup.app.updateUrl(fips);
    d3.selectAll('#interactive button').property('disabled', true);
    if (fips.length == 4) {
      fips = '0'+fips;
    }
    d3.select('#recsWrapper').style('display', 'none');
    // recommendatinos are pre-computed for every county in the US
    var topTeams = OurCup.data.recommendations[fips.toString()];
    // title shows location
    var titleText = "Top Teams for<br />"+countyName+", "+stateCode;
    d3.select('#recsTitle').html(titleText);
    // intro summarizes recommendations
    var introText = "Many of your neighbors are from ";
    var teamNames = topTeams.map(t => {
      var teamInfo = OurCup.data.teams[t];
      return teamInfo.flag + " " + teamInfo.name;
    })
    introText += teamNames[0] + ", " + teamNames[1] + " and " + teamNames[2] + ".";
    d3.select('#recsSummary').html(introText);
    // one card for each team
    var content = "";
    topTeams.forEach((team, index) => {
      d3.select('#team-card-'+team)
        .style('display', 'block');
      var teamInfo = OurCup.data.teams[team];
      var foodQuery = teamInfo.demonym;
      if (teamInfo.foodSearch) {
        foodQuery += ", "+teamInfo.foodSearch;
      }
      var yelpUrl = "https://www.yelp.com/search?find_desc="+foodQuery+
                    "&find_loc="+encodeURIComponent(countyName)+"%2C+"+stateCode;
      content+= "<div class=\"col-md-4\" class=\"team-card\" id=\"team-card-BRA\"><div class=\"team\">";
      content+= "<h3>"+teamInfo.name+"</h3>";
      content+= "<span class=\"flag\">"+teamInfo.flag+"</span>";
      content+= "<p>";
      if (teamInfo.intro) {
        content+= teamInfo.intro+" ";
      }
      if (teamInfo.recipeUrl) {
        content+= "🍲 Support a local business - find a <a href=\""+yelpUrl+"\">"+teamInfo.demonym+" restaurant near you on Yelp</a>, ";
        content+= "or make a <a href=\""+teamInfo.recipeUrl+"\">"+teamInfo.demonym+" recipe from epicurious</a> for dinner tonight. ";
      }
      if (teamInfo.wikipediaUrl) {
        content+= "📖 Learn about <a href=\""+teamInfo.wikipediaUrl+"\">"+teamInfo.name+" on Wikipedia</a>, ";
        content+= "or read from some local journalists on <a href=\""+teamInfo.globalVoicesUrl+"\"> Global Voices "+teamInfo.name+"</a>. ";
      }
      if (teamInfo.spotify) {
        content+= "🎵 Use Spotify to listen to "+teamInfo.spotify.map(i => "<a href=\""+i.url+"\">"+i.name+"</a>").join(", or ")+". ";
      }
      if (teamInfo.teamGuide) {
        content+= "⚽️ Read about the "+teamInfo.demonym+" team on <a href=\""+teamInfo.teamGuide+"\">Guardian Team Guide<a/>";
      }
      content+= "</p>";
      content+= "<p class=\"OurCup.data.fixtures\">"
      content+= "<b>Games to watch</b>"
      content+= "<ul>";
      OurCup.data.fixtures.filter(i => (i.home_team_country == team) || (i.away_team_country == team)).forEach(i => {
        content+= "<li>";
        content+= OurCup.data.teams[i.home_team_country].flag+" "+i.home_team.name;
        content+= " vs. ";
        content+= OurCup.data.teams[i.away_team_country].flag+" "+i.away_team.name;
        content+= "<br/>";
        content+= "on "+i.datetime.substring(0,10);
        content+= "</li>";
      })
      content+= "</ul>";
      content+= "</p>";
      content+= "</div></div>";
    });
    delay(1).then(() => {
      d3.select('#interactive').node().scrollIntoView();
      OurCup.app.updateStatus(true, "Located. Gathering census data...");
      return delay(1000);
    }).then(() => {
      OurCup.app.updateStatus(true, "Doing some math...");
      return delay(1000);
    }).then(() => {
      OurCup.app.updateStatus(true, "Calculating top teams...");
      return delay(1000);
    }).then(() => {
      OurCup.app.updateStatus(true, "Getting fixtures...");
      return delay(1000);
    }).then(() => {
      OurCup.app.updateStatus(false, "Ready");
      d3.select('#countryCardWrapper').html(content);
      d3.select('#recsWrapper').style('display', 'block');
      d3.selectAll('#interactive button').property('disabled', false);
      d3.select('#recsWrapper').node().scrollIntoView();
    });
  },

  updateStatus: (show, msg) => {
    d3.select("#statusWrapper").style("display", (show) ? "block" : "none");
    d3.select("#status").html(msg);
  },

};

// https://stackoverflow.com/questions/39538473/using-settimeout-on-promise-chain
const delay = (t, v) => new Promise(resolve => setTimeout(resolve, t, v));
