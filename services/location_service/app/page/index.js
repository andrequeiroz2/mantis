// In the following example, markers appear when the user clicks on the map.
// Each marker is labeled with a single alphabetical character.

let marker;
let coordinates;

function initMap() {
  const bangalore = { lat: -12, lng: -55 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 6,
    center: bangalore,
    mapTypeId: "terrain",
  });

  map.addListener("click", (mapsMouseEvent) => {
    addMarker(mapsMouseEvent.latLng, map);
    coordinatesGet(mapsMouseEvent)
    });

}

// Adds a marker to the map.
function addMarker(location, map) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.
  if (marker !== undefined) {
    marker.setMap(null);
  }
  marker = new google.maps.Marker({
    position: location,
    map: map,
  });
}

function addMarkerNull(location){
    const marker = new google.maps.Marker({
    position: location,
    map: map,
  });
}

function coordinatesGet(mapsMouseEvent){
    coordinates = JSON.stringify(mapsMouseEvent.latLng.toJSON());
    console.log(coordinates);
}



window.initMap = initMap;