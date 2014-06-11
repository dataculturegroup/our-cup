
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
    $('#oc-loading').hide();
    OurCup.log(position.coords.latitude+","+position.coords.longitude);
    $( "#oc-results" ).load("/picks/location/"+position.coords.latitude+"/"+position.coords.longitude);
    OurCup.log("Wrote location-based results")
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
    $( "#oc-results" ).load("/select-zipcode");
  },

  onPickGamesWithZip: function(){
    var zip = $("#oc-zipcode").val();
    OurCup.log('Checking games with zip '+zip);
    $( "#oc-results" ).load("/picks/zipcode/"+zip);
  },

  log: function(str){
    console.log("OurCup: "+str);
  }

};
