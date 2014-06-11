
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
    OurCup.log(position.coords.latitude+","+position.coords.longitude);
    $('#oc-loading').hide();
  },

  onGeoLocateError: function(error){
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

  log: function(str){
    console.log("OurCup: "+str);
  }

};
