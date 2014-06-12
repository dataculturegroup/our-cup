
OurCup = {

  initialize: function(){
    OurCup.log("initialize");
    OurCup.geolocate();
  },

  geolocate: function(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(OurCup.onGeoLocateSuccess,OurCup.onGeoLocateError);
    } else {
        OurCup.onGeoLocateError("unsupported");
    }
  },

  onGeoLocateSuccess: function(position){
    $('#oc-results').hide();
    $('#oc-loading').show();
    OurCup.log(position.coords.latitude+","+position.coords.longitude);
    OurCup.updateResultsFrom("/picks/location/"+position.coords.latitude+"/"+position.coords.longitude);
  },

  onGeoLocateError: function(error){
    $('#oc-loading').hide();
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
    OurCup.updateResultsFrom("/select-zipcode");
  },

  onPickGamesWithZip: function(){
    var zip = $("#oc-zipcode").val();
    OurCup.log('Checking games with zip '+zip);
    OurCup.updateResultsFrom("/picks/zipcode/"+zip);
  },

  updateResultsFrom: function(url){
    $('#oc-results').hide();
    $('#oc-loading').show();
    $( "#oc-results" ).load(url, function(){
      $('#oc-loading').hide();
      $('#oc-results').show();
    });
  },

  log: function(str){
    console.log("OurCup: "+str);
  }

};
