
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
    const stateCounties = OurCup.data.counties.filter(c => c.state == state);
    const options = stateCounties.map(c => "<option value=\""+c.fips+"\">"+c.name+"</option>")
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
    const topTeamNames = OurCup.data.recommendations[fips.toString()];
    const topTeams = topTeamNames.map(t => OurCup.data.teams[t]);

    // title shows location
    const titleText = "Top Teams for<br />"+countyName+", "+stateCode;
    d3.select('#recsTitle').html(titleText);

    // intro summarizes recommendations
    let introText = "Many of your neighbors are from ";
    let teamNames = topTeams.map(t => t.flag + " " + t.name);
    introText += teamNames[0] + ", " + teamNames[1] + " and " + teamNames[2] + ". ";
    const shareLink = "https://dataculture.northeastern.edu/ourcup/?fips="+fips;
    const tweetLink = "https://twitter.com/intent/tweet?text="+encodeURIComponent("My "+countyName+", "+stateCode+" neighbors support "+
      topTeams.map(t => t.flag).join(" ")+" #worldcup. Visit "+shareLink+" to explore their culture - food, news & music. "+
      "(#ourcup via @rahulbot)");
    introText += "<a href=\""+tweetLink+"\" target=_blank>Share on Twitter</a>";
    d3.select('#recsSummary').html(introText);

    // one card for each team
    let content = "";
    topTeams.forEach(t => {
      let foodQuery = t.demonym;
      if (t.foodSearch) {
        foodQuery += ", "+t.foodSearch;
      }
      const yelpUrl = "https://www.yelp.com/search?find_desc="+encodeURIComponent(foodQuery)+
                    "&find_loc="+encodeURIComponent(countyName)+"%2C+"+stateCode;
      const yummlyUrl = "https://www.yummly.com/recipes?q="+encodeURIComponent(foodQuery);
      content+= "<div class=\"col-md-4\" class=\"team-card\" id=\"team-card-BRA\"><div class=\"team\">";
      content+= "<h3>"+t.name+"</h3>";
      content+= "<span class=\"flag\">"+t.flag+"</span>";
      content+= "<p>";
      if (t.intro) {
        content+= t.intro+" ";
      }
      content+= "🍲 Support a local business - find a <a target=_blank href=\""+yelpUrl+"\">"+t.demonym+" restaurant near you on Yelp</a>, ";
      content+= "or make a <a target=_blank href=\""+yummlyUrl+"\">"+t.demonym+" recipe from Yummly</a>. ";
      if (t.wikipediaUrl) {
        content+= "📖 Learn about <a target=_blank href=\""+t.wikipediaUrl+"\">"+t.name+" on Wikipedia</a>, ";
        content+= "or read from some local journalists on <a target=_blank href=\""+t.globalVoicesUrl+"\"> Global Voices "+t.name+"</a>. ";
      }
      if (t.spotify) {
        content+= "🎵 Use Spotify to listen to "+t.spotify.map(i => "<a target=_blank href=\""+i.url+"\">"+i.name+"</a>").join(", or ")+". ";
      }
      if (t.teamGuide) {
        content+= "⚽️ Read about the "+t.demonym+" team on <a target=_blank href=\""+t.teamGuide+"\">Guardian Team Guide<a/>. ";
      }
      content+= "See a map of <a href=\"#immigrant-map\" onClick=\"d3.select('#"+t.alpha3+"-map').style('display','block');return false;\"> "+t.demonym+" immigrants live</a> across the US.";
      content+= "</p>";
      content+= "<div id=\""+t.alpha3+"-map\" style=\"display:none\">"+
                "<p><b>Map of "+t.demonym+" immigrants</b>"+
                "<img width=\"100%\" src=\"images/map-raw-pop/"+t.alpha3+".png\" alt=\"map of US counties showing where the most "+t.demonym+" immigrants live \">"+
                "</p></div>";
      content+= "<p class=\"OurCup.data.fixtures\">"
      content+= "<b>Games to watch</b>"
      content+= "<ul>";
      OurCup.data.fixtures.filter(i => (i.home_team_country == t.alpha3) || (i.away_team_country == t.alpha3)).forEach(i => {
        content+= "<li>" +
                  i.datetime.substring(5,7)+"/"+i.datetime.substring(8,10)+": "+
                  OurCup.data.teams[i.home_team_country].flag+" "+i.home_team.name+
                  " vs. "+
                  OurCup.data.teams[i.away_team_country].flag+" "+i.away_team.name+
                  "</li>";
      })
      content+= "</ul>";
      content+= "</p>";
      content+= "</div></div>";
    });

    // show user feedback so they understand what went into this
    delay(1).then(() => {
      d3.select('#interactive').node().scrollIntoView();
      OurCup.app.updateStatus(true, "Gathering census data...");
      return delay(1000);
    }).then(() => {
      OurCup.app.updateStatus(true, "Doing some math...");
      return delay(1000);
    }).then(() => {
      OurCup.app.updateStatus(true, "Calculating top teams...");
      return delay(1000);
    }).then(() => {
      OurCup.app.updateStatus(true, "Finding games...");
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
