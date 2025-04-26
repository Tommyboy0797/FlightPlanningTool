// Initialize the map
var map = L.map('map').setView([51.505, -0.09], 6);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var smallAirportIcon = L.icon({
    iconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAANCAYAAACgu+4kAAABgUlEQVR4nIWRzStEURjGf2ecGeZeG8zOR/wL7oaSjYXl4N5SIkqJjJ2FnWwUNiwxStlQ5zY+/gBLWZyy8bGRFBnjKyULMcfCjO6Mwbs5nZ7n97xPvWK6h3/Hc7w40AUsKa2Ogpr8HXJjIJqBMDAJtAH7wN8BruPaAjEPDAPlAekDzEGxX0z3gOd4nUAcWAdmgY6gyY7ZROwIT5dPFwbT4ms/k9dCuTcBjAGHpeD6oSS1fStY1VaTQMwE9XzACDAFPAdFq8aifjCJjEgyqXFeH18BPNdxywoClFY3Sqs54PobrrZoGFxDlkvuUgkyZ9+tqwC7uEF+rgCiVdGvzRWS++0Et6e3QU9WINo9x5OlAjZDMkRd/yrhaJiH3QnShTB8nXUP2IaiMxrMRvY923uzNdpZGaskfZoGUwCfAwvAALDzo4Gv/Xeg+yXzsp8+KYA/gJTBtCutlpVWbQaT/NEg1+MNRGPuMwpcGMyxr/3roMvXvikZYEAKWARaDWYlb/xtPgFd9n9MLLgfqAAAAABJRU5ErkJggg==', // Your base64 data here
});

var mediumAirportIcon = L.icon({
    iconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAANCAYAAACgu+4kAAAABmJLR0QA4ADgAODYf054AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1ggQEQ8TdhjdmgAAAB10RVh0Q29tbWVudABDcmVhdGVkIHdpdGggVGhlIEdJTVDvZCVuAAABiElEQVQoz42SPUgjURSFv6dvNGIqTTatgqJYWimYuLLFNguxsNiZVhJcEjsL220srLTNFCsITrBY/GFZoqCFiG7jTxGNwmCzWkiaWInBvTYTmUmi7G0ej3vOveeddxT/UU46nwQmgWUz9/XM39NvklJOBKWGAQOYA8aAfeD9AWspp1MptQhMA+2+1jMiR/V45Un8DCSBFWAB+OQHxQZjhKNh3AP3RkRGLNu8r1eQBb4A3+o3xAY+EM+MoQ1N5a7SW3bL3/24Fu9MA/NAxU+O9keJZ+LoNk3x9wVltwwwtZZyWgNP8LldBIYAIn0RPs6Oo0Oay0KJ85/nr16ISJdlmw9+BbX6C9Dd2814NoEOaUo7ATLAP6VUwknndbMBeSNkkMjEMToMrveuOQuS8b51G9hoGCAiq9XHauH4xx9Ku1ecrJ+CBMguMAMcApsNHng+dAC/gIlABmBLRLKWbd55eVGWbUpjEkWeUKrHu80AN4IUrZx564dZtilNkygKrWAJGBWRXA34Vr0A5+eD8J8Ey48AAAAASUVORK5CYII=',
});

var largeAirportIcon = L.icon({
    iconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAANCAYAAACgu+4kAAABfklEQVR4nIXRMUtVcRzG8c/pnqt1jkOaLZVQb+G6FIiLg6PFPdSSNARhZFtDm7QE1VJjdoWgpeEcTHsBjtFwLy0VDSFE0jXLCMEhvJ0GPXC6V+tZ/vz5Ps/DA7+AOf9TfTSZwnk8yprpmzILDwzVkmGBGqq4hTGs4N8F9VoSC9zHVfSXUEfuVbc/YE59NJnEFJ7iLibKpoHhAX1Rn81Pm6tyZ7NW+rVgh/beWVzH657wsVhj+ZT57IRoMDojcKfMi4JruI2fZRgPxRrLI8K+0I3LG7Z/bENSryWVvwqyZvola6b3sFaAaCiysDwi7A/NTn+z/mG9QIOIuxcU+gzR0cjC0ojw8G64/b5d9vwWGK+PJuF+Bc8rYcWTxZOqR6puXvneHWb3rC/xgu4z5p51djqXZi62J+Pjsfa7nvBHPMA0lnoWZK10Bxe2NrZWusIdLMqNZ830cdZMx+QavQt2V/wSOL33m8Eq3mbNdK1sy1ppvn9BIMRDnJObL4wH6Q+YX3T83b7+/AAAAABJRU5ErkJggg=='
});

let selected_waypoints = [];
let waypoint_data_values = [];
let distance = 0;
let custom_waypoint_store = []; // stores custom points { name, lat, lng }


document.getElementById('dataForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        gwt: document.getElementById('gwt').value,
        get_to_factor: document.getElementById('get_to_factor').value,
        get_rwy_available: document.getElementById('get_rwy_available').value,
        get_rwy_slope: document.getElementById('get_rwy_slope').value,
        rsc: document.getElementById("get_rsc").value,
        rcr: document.getElementById("get_rcr").value,
        atcsoper: document.getElementById("atcs_oper").checked,
        asoper: document.getElementById("anti_skid_oper").checked,
        dragindex: document.getElementById("get_di").value,
        origin: dep_ap,
        runwy: document.getElementById("enterRwy").value,
    };
    
    const params = new URLSearchParams(formData);
    
    fetch(`/get_data?${params}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('gross_weight_txt').textContent = `${data.gross_weight_text} lbs`;
            document.getElementById('takeofffactortext').textContent = data.takeoff_factor_text;
            document.getElementById('runway_avail_text').textContent = `${data.runway_avail} feet`;
            document.getElementById('runway_slope_text').textContent = `${document.getElementById('get_rwy_slope').value} degrees`;
            document.getElementById('uncorrected_max_eff_TO_dist_text').textContent = `${data.uncorrected_max_eff_TO_dist} feet`;
            document.getElementById('rotation_speed_calculated_text').textContent = `${data.rotation_speed_calculated} knots`;
            document.getElementById('corrected_refusal_speed').textContent = data.corrected_refusal_speed;
        })
        .catch(error => console.error('Error:', error));
});


// Store markers for each airport type
var smallAirportsMarkers = [];
var mediumAirportsMarkers = [];
var largeAirportsMarkers = [];

function loadAirports(filters) {

const filterParams = new URLSearchParams(filters);
fetch(`/fetch_airports?${filterParams}`)
.then(response => response.json())
.then(data => {
    // Initialize marker clusters
    var smallMarkersCluster = L.markerClusterGroup();
    var mediumMarkersCluster = L.markerClusterGroup();
    var largeMarkersCluster = L.markerClusterGroup();

    // Add small airports with clustering
    if (filters.small_ap && data.small_airports) {
        data.small_airports.forEach(airport => {
            var marker = L.marker([airport.lat, airport.lng], { icon: smallAirportIcon });
            marker.bindPopup(`
                <b>${airport.name} (${airport.type})</b> 
                <br>
                <b>${airport.length}</b>
                <button onclick="set_origin_airfield('${airport.name}')">Set as Origin</button>
                <br>
                <button onclick="set_arrival_airfield('${airport.name}')">Set as Arrival</button>
                
            `);
            smallMarkersCluster.addLayer(marker);
        });
    }

    // Add medium airports with clustering
    if (filters.medium_ap && data.medium_airports) {
        data.medium_airports.forEach(airport => {
            var marker = L.marker([airport.lat, airport.lng], { icon: mediumAirportIcon });
            marker.bindPopup(`
                <b>${airport.name}</b> (${airport.type})<br>
                <button onclick="set_origin_airfield('${airport.name}')">Set as Origin</button>
                <br>
                <button onclick="set_arrival_airfield('${airport.name}')">Set as Arrival</button>
            `);
            mediumMarkersCluster.addLayer(marker);
        });
    }

    // Add large airports with clustering
    if (filters.large_ap && data.large_airports) {
        data.large_airports.forEach(airport => {
            var marker = L.marker([airport.lat, airport.lng], { icon: largeAirportIcon });
            marker.bindPopup(`
                <b>${airport.name}</b> (${airport.type})<br>
                <button onclick="set_origin_airfield('${airport.name}')">Set as Departure</button>
                <br>
                <button onclick="set_arrival_airfield('${airport.name}')">Set as Arrival</button>
            `);
            largeMarkersCluster.addLayer(marker);
        });
    }

    // Clear previous marker clusters
    map.eachLayer(layer => {
        if (layer instanceof L.MarkerClusterGroup) {
            map.removeLayer(layer);
        }
    });

    // Add all clusters to the map
    map.addLayer(smallMarkersCluster);
    map.addLayer(mediumMarkersCluster);
    map.addLayer(largeMarkersCluster);
})
.catch(error => console.error('Error fetching airport data:', error));
}

// Update map on form submission
document.getElementById('filterForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var filters = {
        small_ap: document.getElementById('small_ap').checked,
        medium_ap: document.getElementById('medium_ap').checked,
        large_ap: document.getElementById('large_ap').checked,
    };
    loadAirports(filters);
});

// Load initial airports with default filters
loadAirports({ small_ap: true, medium_ap: true, large_ap: true, show_sids: true, });

enter_rwy_dropdown = document.getElementById("enterRwy");
enter_sid_dropdown = document.getElementById("chooseSid");
enter_arr_runway = document.getElementById("chooseArrRw");

let dep_ap = "0";
let final_sid_point = "";

function set_origin_airfield(airportname){
    dep_ap = airportname;

    fetch("/set_origin", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({send_str: airportname}), // send airport name as the body
    })

    fetch("/weather_info", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({send_str: airportname}), // send airport name as the body
    })

    .then(response => response.json())
    .then(data => {

        document.getElementById("rawMetar").innerText = data.raw_metar
        document.getElementById("metarTime").innerText = data.time
        document.getElementById("metarRemarks").innerText = data.remarks
        document.getElementById("metarStation").innerText = data.station
        document.getElementById("metarAltimeter").innerText = data.altimeter
        document.getElementById("metarTemp").innerHTML = data.temp
        document.getElementById("metarHumidity").innerText = data.humidity
        document.getElementById("metarDewpoint").innerText = data.dewpoint
        document.getElementById("metarVisibility").innerText = data.visibility
        document.getElementById("metarClouds").innerText = data.clouds
        document.getElementById("metarWind").innerText = data.wind
    })


    fetch(`/get_runways`, {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({send_str: airportname}), // send airport name as the body
    })

    .then(response => response.json())
    .then(data => {

        function drawCircle(center, radiusMiles) {
            let radiusMeters = radiusMiles * 1609.34; // Convert miles to meters

            if (window.originCircle) {
                map.removeLayer(window.originCircle);
            }
        
            window.originCircle = L.circle([center.lat, center.lng], {
                color: "black",
                fillColor: "white",
                fillOpacity: 0,
                radius: radiusMeters
            }).addTo(map);
        }


        let runways_list = data.origin_runways;

        let range = 2440 * (document.getElementById("fuel_slider").value / 100);

        enter_rwy_dropdown.innerHTML = "";

        runways_list.forEach(runway => {
            enter_rwy_dropdown.options[enter_rwy_dropdown.options.length] = new Option(runway, runway);
        })

        dep_rwy_change.call(enter_rwy_dropdown); // make sure the function calls straight away so that the user doesnt have to select a runway, then back to their desired to display SIDs

        let center = { lat: data.af_latlng[0].lat, lng: data.af_latlng[0].lng };

        document.getElementById("show_rr").onchange = function () {
            if (this.checked) {
                let range = 2440 * (document.getElementById("fuel_slider").value / 100);
                drawCircle(center,range);
            }
            else {
                if (window.originCircle) {
                    map.removeLayer(window.originCircle);
                }
            }
        }

        document.getElementById("fuel_slider").oninput = function(){
            document.getElementById("fuel_value").innerText = document.getElementById("fuel_slider").value;
            let range = 2440 * (document.getElementById("fuel_slider").value / 100);
            if (document.getElementById("show_rr").checked) {
                drawCircle(center,range);
            }
        }

    })
    .catch(error => console.error('Error fetching runway data:', error));
};

function dep_rwy_change () {
    if (!this.value) return; // Prevent sending empty selections
        fetch("/return_runway", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({runwy: {send_str: this.value}, origin: {send_str: dep_ap}}),
        })
        .then(response => response.json())
        .then(data => {

            enter_sid_dropdown.innerHTML = "";
            data.sids.forEach(sids => {
                enter_sid_dropdown.options[enter_sid_dropdown.options.length] = new Option(sids, sids);
            })
        })
        
        fetch("/airfield_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({origin: {send_str: dep_ap},runwy: {send_str: this.value}}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error:", data.error);
                document.getElementById("airfield_info").textContent = "No airfield or runway selected.";
                return;
            }
            if (data.origin_latlng.length > 0){ // if there is no SID available for that airfield, just connect the route to the center of it
                final_sid_point = {
                    lat: data.origin_latlng[0].lat,
                    lng: data.origin_latlng[0].lng
                };
            };
        })
        .catch(error => console.error("Error fetching runway data:", error));
};
document.getElementById("enterRwy").onchange = dep_rwy_change;

document.getElementById("chooseSid").onchange = function () {
    if (window.sid_waypoints && window.sid_waypoints.length > 0) {
        window.sid_waypoints.forEach(marker => map.removeLayer(marker));
    }
    let previousPoint = null;
    // Reset the marker array
    window.sid_waypoints = [];
    fetch("/return_sid", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({select_sid: {send_str: this.value}, origin: {send_str: dep_ap}, runwy: {send_str: document.getElementById("enterRwy").value}}),
    })  
    
    .then(response => response.json())
    .then(data => {
        
        if (data.selected_sid_points.length >= 1) { // only do this when there IS infact a SID
            console.log("There is a SID!");
            data.selected_sid_points.sort((a, b) => a.sequence_number - b.sequence_number);
            final_sid_point = data.selected_sid_points[data.selected_sid_points.length - 1] // get the final sid point, and as it starts at 0, sub 1
        };
        data.selected_sid_points.forEach(point => {
            let sid_waypoint = L.marker([point.lat, point.lng])
                .bindPopup(`<b>${point.ident}</b>`)
                .addTo(map);
            let sid_lines = L.polyline(data.selected_sid_points, { color: "blue"}).addTo(map);
            if (previousPoint) {
                distance += L.latLng(point.lat, point.lng).distanceTo(L.latLng(previousPoint.lat, previousPoint.lng));
            }
        
            previousPoint = point;
            window.sid_waypoints.push(sid_waypoint, sid_lines);
            
        });
    })
};

let arrivalairport = "";
let star_init_point = "";

function set_arrival_airfield(arrival_field) {
    arrivalairport = arrival_field
    fetch("/return_arrival_airport", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({send_str: arrival_field}), // send airport name as the body
    })
    
    .then(response => response.json())
    .then(data => {

        enter_arr_runway.innerHTML = "";

        data.arrival_runways.forEach(runway => {
            enter_arr_runway.options[enter_arr_runway.options.length] = new Option(runway, runway);
        
        display_star.call(enter_arr_runway);
        
        if (data.arrival_latlng.length > 0){ // if there is no STAR available for that airfield, just connect the route to the center of it
            star_init_point = {
                lat: data.arrival_latlng[0].lat,
                lng: data.arrival_latlng[0].lng
            };
        };
        })
    })
}

document.getElementById("chooseArrRw").onchange = display_star;

function display_star () {

    fetch("/handle_stars", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({selected_runway: {send_str: this.value},arrival_airfield: {send_str: arrivalairport}}), 
    })
     
    .then(response => response.json())
    .then(data => {

        chooseArrStar.innerHTML = "";

        data.arrival_stars.forEach(star => {
            chooseArrStar.options[chooseArrStar.options.length] = new Option(star, star);
        })

    })
}

document.getElementById("chooseArrStar").onchange = function () {

    if (window.star_waypoints && window.star_waypoints.length > 0) {
        window.star_waypoints.forEach(marker => map.removeLayer(marker));
    }
    let previousPoint = null;
    // Reset the marker array
    window.star_waypoints = [];

    fetch("/send_star_data", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({selected_star: {send_str: this.value}, arrival_airfield: {send_str: arrivalairport}, arrival_runway: {send_str: document.getElementById("chooseArrRw").value}}), 
    })

    .then(response => response.json())
    .then(data => {
     
        document.getElementById("userRoute").innerHTML = data.route

        
        if (data.selected_star_data.length >= 1){ // only do this when there is STARs
            data.selected_star_data.sort((a, b) => a.sequence_number - b.sequence_number);
            star_init_point = data.selected_star_data[0]; // access first STAR point
        };

        data.selected_star_data.forEach(point => {
            let star_waypoint = L.marker([point.lat, point.lng])
                .bindPopup(`<b>${point.ident}</b>`)
                .addTo(map);
            let star_lines = L.polyline(data.selected_star_data, { color: "red"}).addTo(map);
            if (previousPoint) {
                distance += L.latLng(point.lat, point.lng).distanceTo(L.latLng(previousPoint.lat, previousPoint.lng));
            }
        
            previousPoint = point;
            window.star_waypoints.push(star_waypoint, star_lines)

        });

    })

}

document.getElementById("enter_waypoint_box").onchange = function () {

    if (window.waypoint_markers && window.waypoint_markers.length > 0) {
        window.waypoint_markers.forEach(marker => map.removeLayer(marker));
    }

    window.waypoint_markers = [];

    fetch("/waypoint_info", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({send_str: this.value}), 
    })
    .then(response => response.json())
    .then(data => {

        data.waypointdata.forEach(point => {
            let waypoint_marker = L.marker([point.lat, point.lng])
                .bindPopup(`<b>${point.name}<br> ${point.usage}<br>${point.icao}${point.area} <br> <button onclick="add_wp_to_route('${point.name}')">Add to Route</button></b>`) // call the function + send WP name
                .addTo(map);
            let new_view = map.panTo(new L.LatLng(point.lat, point.lng)) // recenter view onto waypoint
            window.waypoint_markers.push(waypoint_marker, new_view)

        
        });
    })


}

function add_wp_to_route(waypoint_name) {

    selected_waypoints.push(waypoint_name);
    console.log(selected_waypoints);
    fetch("/append_route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({waypoint: selected_waypoints, origin: {send_str: dep_ap}, runwy: {send_str: document.getElementById("enterRwy").value}, select_sid: {send_str: document.getElementById("chooseSid").value}, selected_star: {send_str: document.getElementById("chooseArrStar").value},selected_runway: {send_str: document.getElementById("chooseArrRw").value} ,arrival_airfield: {send_str: arrivalairport}}),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("userRoute").innerHTML = data.route;
        display_waypoints(); 
    });
}


function display_waypoints() {
    let waypoint_data_values = []; 
    let previousPoint = null;

    let fetchPromises = selected_waypoints.map((wp, index) => {
        // Try to find it in the custom waypoint store first
        let custom_wp = custom_waypoint_store.find(cwp => cwp.name === wp);
        if (custom_wp) {
            waypoint_data_values.push({
                index: index,
                lat: custom_wp.lat,
                lng: custom_wp.lng,
                name: custom_wp.name,
                usage: custom_wp.usage,
                icao: "CTM",
                area: "",
                notes: custom_wp.notes,
                is: "Custom Waypoint"
            });
            return Promise.resolve(); // skip server call
        }
        return fetch("/waypoint_info", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ send_str: wp }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.waypointdata.length > 0) {
                waypoint_data_values.push({ 
                    index: index, // this adds index as an option in the data
                    ...data.waypointdata[0] // "..." is a spread operator which just makes the code cleaner
                });
            }
        });
    });

    Promise.all(fetchPromises).then(() => {
        waypoint_data_values.sort((a, b) => a.index - b.index); // sorting waypoints by index to avoid the triangle issue

        if (window.waypoint_markers && window.waypoint_markers.length > 0) {
            window.waypoint_markers.forEach(marker => map.removeLayer(marker));
        }

        window.waypoint_markers = [];

        waypoint_data_values.forEach((point, index) => {
            let waypoint_marker = L.marker([point.lat, point.lng]);
            // Check if the waypoint is a custom one
            if (point.is === "Custom Waypoint") {
                // For custom waypoints, display the custom format
                waypoint_marker = waypoint_marker.bindPopup(
                    `<b>${point.name}</b><br>` +
                    `<i>${point.usage}</i><br>` +
                    `<b>Lat:</b> ${point.lat.toFixed(6)}<br>` +
                    `<b>Lng:</b> ${point.lng.toFixed(6)}<br>` +
                    (point.notes ? `<b>Notes:</b> ${point.notes}` : "")
                );
            } else {
                // For normal waypoints, use the default format
                waypoint_marker = waypoint_marker.bindPopup(
                    `<b>${point.name}<br> ${point.usage}<br>${point.icao}${point.area}<br>` +
                    `<button onclick="remove_wp_from_route('${point.lat}, ${point.lng}')">Remove</button>`
                );
            }

            waypoint_marker.addTo(map);
            if (previousPoint) {
                distance += L.latLng(point.lat, point.lng).distanceTo(L.latLng(previousPoint.lat, previousPoint.lng));
            }
        
            previousPoint = point;
            window.waypoint_markers.push(waypoint_marker);
        });

        if (window.routePolyline) {
            map.removeLayer(window.routePolyline);
        }
        
        let latlngs = waypoint_data_values.map(point => [point.lat, point.lng]);

        if (final_sid_point && final_sid_point.lat && final_sid_point.lng) {
            latlngs.unshift([final_sid_point.lat, final_sid_point.lng]); // "unshift" adds to start of array 
        }

        if (star_init_point && star_init_point.lat && star_init_point.lng) {
            latlngs.push([star_init_point.lat, star_init_point.lng]);
            console.log("Star INIT point pushed".latlngs)
            console.log([star_init_point.lat, star_init_point.lng])
        }

        if (latlngs.length > 1) {
            window.routePolyline = L.polyline(latlngs, { color: "green" }).addTo(map);
        }

        console.log("Updated Route with Waypoints:", latlngs);
        console.log("Distance:", distance / 1609.34);
        
    });
}

function remove_wp_from_route(lat, lng) {

    waypoint_data_values = waypoint_data_values.filter(wp => wp != lat,lng);
    console.log(waypoint_data_values, "removed from route");
    display_waypoints();
    
}

document.getElementById("enter_airway_box").onchange = function () {

    if (window.airway_markers && window.airway_markers.length > 0) {
        window.airway_markers.forEach(marker => map.removeLayer(marker));
    }

    window.airway_markers = [];
    
    fetch("/get_airways", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, 
        body: JSON.stringify({send_str: this.value})
    })
    .then(response => response.json())
    .then(data => {

        data.airway_info.sort((a, b) => a.seqno - b.seqno); // make sure data is sorted to avoid triangle stuff

        data.airway_info.forEach(point => {
            let waypoint_marker = L.marker([point.lat, point.lng])
                .bindPopup(`<b>${point.ident}<br> ${point.route_ident}</b>`)
                .addTo(map);
            let airway_polyline = L.polyline(data.airway_info, {color: 'purple'}).addTo(map)
            let new_view = map.panTo(new L.LatLng(point.lat, point.lng))
            window.airway_markers.push(airway_polyline,waypoint_marker, new_view)
        })

    })
    .catch(error => console.error("Error fetching airway data:", error));
};


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('routePlanningNav').addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('routePlanningPage').classList.add('active-page');
        document.getElementById('routePlanningPage').classList.remove('inactive-page');
        document.getElementById('toldPage').classList.add('inactive-page');
        document.getElementById('toldPage').classList.remove('active-page');
        document.getElementById('flightInfoPage').classList.add('inactive-page');
        document.getElementById('flightInfoPage').classList.remove('active-page');

        document.getElementById('routePlanningNav').classList.add('active');
        document.getElementById('toldNav').classList.remove('active');
    });

    document.getElementById('toldNav').addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('routePlanningPage').classList.add('inactive-page');
        document.getElementById('routePlanningPage').classList.remove('active-page');
        document.getElementById('toldPage').classList.add('active-page');
        document.getElementById('toldPage').classList.remove('inactive-page');
        document.getElementById('flightInfoPage').classList.add('inactive-page');
        document.getElementById('flightInfoPage').classList.remove('active-page');

        document.getElementById('routePlanningNav').classList.remove('active');
        document.getElementById('toldNav').classList.add('active');
    });
    document.getElementById('flightInfoNav').addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('routePlanningPage').classList.add('inactive-page');
        document.getElementById('routePlanningPage').classList.remove('active-page');
        document.getElementById('toldPage').classList.add('inactive-page');
        document.getElementById('toldPage').classList.remove('active-page');
        document.getElementById('flightInfoPage').classList.add('active-page');
        document.getElementById('flightInfoPage').classList.remove('inactive-page');

        document.getElementById('routePlanningNav').classList.remove('active');
        document.getElementById('toldNav').classList.remove('active');
        document.getElementById('flightInfoNav').classList.add('active');
    });
});

let debounceTimer;
document.getElementById("enter_airfield_box").addEventListener("input", function () {
    clearTimeout(debounceTimer);  // Reset the timer
    
    let query = this.value.trim();
    if (query.length === 0) {
        document.getElementById("autocomplete_list").style.display = "none";
        return;
    }

    debounceTimer = setTimeout(() => {
        fetch("/airfield_autocomplete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ send_str: query })
        })
        .then(response => response.json())
        .then(data => {
            let list = document.getElementById("autocomplete_list");
            list.innerHTML = "";

            data.autocorrect_data.forEach(airport => {
                let item = document.createElement("div");
                item.classList.add("autocomplete-item");
            
                item.innerHTML = `<b>${airport.name || "Unknown"}</b> (${airport.icao || "N/A"})`;
            
                item.addEventListener("click", function () {
                    document.getElementById("enter_airfield_box").value = airport.icao; // Autofill
                    list.style.display = "none";
            
                    if (/^[A-Z]{4}$/.test(airport.icao)) { // If ICAO code
                        fetchEnteredAirfield(airport.icao);
                    }
                });
            
                list.appendChild(item);
            });
            
            list.style.display = data.autocorrect_data.length > 0 ? "block" : "none";
        });
    }, 200);
});

function fetchEnteredAirfield(icao) {
    fetch("/entered_airfield", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ send_str: icao })
    })
    .then(response => response.json())
    .then(data => {
        let airfield = data.airfield_data[0]; 
        let icon_type = null;

        if (airfield.type === "large_airport") {
            icon_type = largeAirportIcon;
        } else if (airfield.type === "medium_airport") {
            icon_type = mediumAirportIcon;
        } else if (airfield.type === "small_airport") {
            icon_type = smallAirportIcon;
        }

        data.airfield_data.forEach(point => {
            let marker = L.marker([point.lat, point.lng], { icon: icon_type });

            marker.bindPopup(`
                <b>${point.name}</b> (${point.type})<br>
                <button onclick="set_origin_airfield('${point.name}')">Set as Departure</button>
                <br>
                <button onclick="set_arrival_airfield('${point.name}')">Set as Arrival</button>
            `);

            marker.addTo(map);
            map.setView(new L.LatLng(point.lat, point.lng), 10);

            if (!window.markers) {
                window.markers = [];
            }

            window.markers.push(marker);
        });
    });
}

document.addEventListener("click", function (event) {
    if (!event.target.closest("#enter_airfield_box") && !event.target.closest("#autocomplete_list")) {
        document.getElementById("autocomplete_list").style.display = "none";
    }
});

document.addEventListener("DOMContentLoaded", function (){ // make sure tghe page is loaded before the function can be done
    document.getElementById("nearest_waypoint_button").onclick = function () {

        document.getElementById("map").style.cursor = "crosshair"; // set the cursor to a crosshair so people know theyre in that mode
    
        map.once('click', function(e){ // only fires once so they need to click the button again to go again
    
            fetch("/nearest_waypoints", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ lat: {send_int: e.latlng.lat}, lng:{send_int: e.latlng.lng} })
            })
            .then(response => response.json())
            .then(data => {
        
                console.log(data.waypoints);
                document.getElementById("waypointList").innerText = "";
                
                // Clear existing markers
                window.nearbywaypoint_markers = window.nearbywaypoint_markers || [];
                window.nearbywaypoint_markers.forEach(marker => marker.remove());
                window.nearbywaypoint_markers = [];

                data.waypoints.forEach((point) => {
                    let waypoint_marker = L.marker([point.lat, point.lng])
                        .bindPopup(`<b>${point.name} <br> <button onclick="add_wp_to_route('${point.name}')">Add to Route</button></b>`) // call the function + send WP name
                        .addTo(map);
                    window.nearbywaypoint_markers.push(waypoint_marker)
                });

                data.waypoints.forEach((wp) => {
                    let item = document.createElement("div");
                    item.classList.add("waypoint-item");
                    item.textContent = `${wp.name} - ${wp.dist} miles`;
                    document.getElementById("waypointList").appendChild(item);
                });

                const mapContainer = document.getElementById("map");
                const boxWidth = document.getElementById("waypointBox").offsetWidth;
                const boxHeight = document.getElementById("waypointBox").offsetHeight;

                const posX = e.originalEvent.clientX + 10; 
                const posY = e.originalEvent.clientY + 10; 

                document.getElementById("waypointBox").style.left = `${posX}px`;
                document.getElementById("waypointBox").style.top = `${posY}px`;

                document.getElementById("waypointBox").style.display = "block";
                
            })
            .finally(() => {
                document.getElementById("map").style.cursor = "auto"; // reset the cursor to whatever it was before

                map.on('contextmenu', function(e) {
                    document.getElementById("waypointBox").style.display = "none";
                    window.nearbywaypoint_markers = window.nearbywaypoint_markers || [];
                    window.nearbywaypoint_markers.forEach(marker => marker.remove());
                    window.nearbywaypoint_markers = [];
                })
            });
        
        })
    
    }

})

document.getElementById("clearMap").addEventListener("click", function() {
    location.reload();
});

let toggle_type = "departure";

document.getElementById("toggleMetar").addEventListener("click", function () {

    toggle_type = toggle_type === "departure" ? "arrival" : "departure"; // "ternary operator", shorthand for if-else statement, If toggle_type is "departure", it changes it to "arrival". Otherwise, it sets toggle_type to "departure"

    document.getElementById("rawMetar").innerText = "Loading..."; // change the text to loading so they know its working when they toggle and not just frozen
    document.getElementById("metarTime").innerText = "Loading...";
    document.getElementById("metarRemarks").innerText = "Loading...";
    document.getElementById("metarStation").innerText = "Loading...";
    document.getElementById("metarAltimeter").innerText = "Loading...";
    document.getElementById("metarTemp").innerText = "Loading...";
    document.getElementById("metarHumidity").innerText = "Loading...";
    document.getElementById("metarDewpoint").innerText = "Loading...";
    document.getElementById("metarVisibility").innerText = "Loading...";
    document.getElementById("metarClouds").innerText = "Loading...";
    document.getElementById("metarWind").innerText = "Loading...";

    let airport_code = toggle_type === "arrival" ? arrivalairport : dep_ap; // send data depending on if departure or arrival is set

    fetch("/weather_info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ send_str: airport_code }), // Send the correct airport code
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("rawMetar").innerText = data.raw_metar; // display data
            document.getElementById("metarTime").innerText = data.time;
            document.getElementById("metarRemarks").innerText = data.remarks;
            document.getElementById("metarStation").innerText = data.station;
            document.getElementById("metarAltimeter").innerText = data.altimeter;
            document.getElementById("metarTemp").innerText = data.temp;
            document.getElementById("metarHumidity").innerText = data.humidity;
            document.getElementById("metarDewpoint").innerText = data.dewpoint;
            document.getElementById("metarVisibility").innerText = data.visibility;
            document.getElementById("metarClouds").innerText = data.clouds;
            document.getElementById("metarWind").innerText = data.wind;
        })
        .catch(error => {
            console.error("Error fetching METAR data:", error);
            document.getElementById("rawMetar").innerText = "Error loading data";
        });
});


document.getElementById("login_submit").addEventListener("click", function (event) {
    const formData = new FormData();
    formData.append("username", document.getElementById("login_username").value);
    formData.append("password", document.getElementById("login_password").value);

    fetch("/login", {
        method: "POST",
        body: formData,
    })
    .then(async response => {
        if (!response.ok) {
            const error = await response.json();
            alert("Login failed: " + error.detail);
            return;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return; // In case login failed

        console.log(data);
        localStorage.setItem("username", data.user);
        localStorage.setItem("signup_date", data.signup_date);
        location.reload(); // Reload the page to reflect login state
    })
    .catch(error => console.error("Error:", error));
});

document.getElementById("signup_submit").addEventListener("click", function (event) {
    const formData = new FormData();
    formData.append("username", document.getElementById("signup_username").value);
    formData.append("password", document.getElementById("signup_password").value);

    fetch("/signup", {
        method: "POST",
        body: formData,
    })
    .then(async response => {
        if (!response.ok) {
            const error = await response.json();
            alert("Signup failed: " + error.detail);
            return;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return; // In case signup failed

        console.log(data);
        localStorage.setItem("username", data.user);
        localStorage.setItem("signup_date", data.signup_date);
        location.reload(); // Reload the page to reflect login state
    })
    .catch(error => console.error("Error:", error));
});

window.addEventListener("DOMContentLoaded", () => {
    console.log("Trying to get profile data")
    const username = localStorage.getItem("username");

    if (username) {
        document.getElementById("profileUsername").innerText = username;

        const signup_date = localStorage.getItem("signup_date");
        document.getElementById("profileMemberSince").innerText = signup_date;
        display_user_routes();
        const authLink = document.getElementById("loginsignupbutton");
        if (authLink) {
            authLink.style.display = "none";
        }

    } else {
        console.warn("Profile data is missing from localStorage");
        const profile = document.getElementById("profile_button");
        if (profile) {
            profile.style.display = "none";
        }
    }
});

document.getElementById("logoutBtn").addEventListener("click", function () {
    localStorage.clear(); // remove all user data
    location.reload(); // reload the page to update UI
});

document.getElementById("saveRoute").addEventListener("click", function(){
    store_routes();
});

function store_routes(){
    fetch("/store_route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({route: {send_str: document.getElementById("userRoute").innerText}, username: {send_str: localStorage.getItem("username")}})
    })
    .then(response => response.json())
    .then(data => {
        display_user_routes();
    });
}

let saved_route_count = 0;

function display_user_routes () {
    fetch("/show_routes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({route: {send_str: document.getElementById("userRoute").innerText}, username: {send_str: localStorage.getItem("username")}})
    })
    .then(response => response.json())
    .then(data => {
        saved_route_count = 0;
        console.log(data.info.routes);
    
        document.getElementById("savedRoutesTable").innerHTML = '';
        
        if (data.info.routes.length === 0){ // if there is no saved routes, say so
            document.getElementById("savedRoutesTable").innerHTML = `<td colspan="5" class="text-center text-muted">No saved routes</td>`
            return;
        }
    
        data.info.routes.forEach(route => { 
            console.log("log")
            saved_route_count = saved_route_count + 1;
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${route.route_name}</td>
                <td>${route.from}</td>
                <td>${route.to}</td>
                <td>${route.last_used}</td>
                <td>
                    <button class="use-route-btn" data-route-id="${route.route_name}" data-route-data="${route.route_data}">Use Route</button>
                    <button class="delete-route-btn" data-route-id="${route.route_name}">
                        <span class="visually-hidden">Delete Route</span>
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;  
            document.getElementById("savedRoutesTable").appendChild(row); // add row to table
            document.getElementById("savedRoutes").innerText = saved_route_count;
        });
    });
}

// Use event delegation for both "use-route-btn" and "delete-route-btn"
document.getElementById("savedRoutesTable").addEventListener("click", function(event) {
    distance = 0;
    // Handle "Use Route" button click
    if (event.target.classList.contains("use-route-btn")) {
        const routeId = event.target.getAttribute("data-route-id");
        const routeData = event.target.getAttribute("data-route-data");
        console.log("route data:",routeData);
        document.getElementById("userRoute").innerText = routeData

        console.log("Using route with ID:", routeId);
        fetch("/route_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({send_str: routeData})
        })
        .then(response => response.json())
        .then(data => {

            console.log(data); // all the data
            console.log(data[0].dep_rwy); // how to access just one part of the data
            set_origin_airfield(data[0].departure); // departure airfield set.

            if (window.sid_waypoints && window.sid_waypoints.length > 0) { // display the SID
                window.sid_waypoints.forEach(marker => map.removeLayer(marker));
            }
            console.log(JSON.stringify({select_sid: {send_str: data[0].SID}, origin: {send_str: data[0].departure}, runwy: {send_str: data[0].dep_rwy}}));
            let arrivalfield = data[0].arrival;
            let previousPoint = null;
            // Reset the marker array
            window.sid_waypoints = [];
            fetch("/return_sid", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({select_sid: {send_str: data[0].SID}, origin: {send_str: data[0].departure}, runwy: {send_str: data[0].dep_rwy}}),
            })  
            
            .then(response => response.json())
            .then(data => {
                
                if (data.selected_sid_points.length >= 1) { // only do this when there IS infact a SID
                    console.log("There is a SID!");
                    data.selected_sid_points.sort((a, b) => a.sequence_number - b.sequence_number);
                    final_sid_point = data.selected_sid_points[data.selected_sid_points.length - 1] // get the final sid point, and as it starts at 0, sub 1
                };
                data.selected_sid_points.forEach(point => {
                    let sid_waypoint = L.marker([point.lat, point.lng])
                        .bindPopup(`<b>${point.ident}</b>`)
                        .addTo(map);
                    let sid_lines = L.polyline(data.selected_sid_points, { color: "blue"}).addTo(map);
                    if (previousPoint) {
                        distance += L.latLng(point.lat, point.lng).distanceTo(L.latLng(previousPoint.lat, previousPoint.lng));
                    }
                
                    previousPoint = point;
                    window.sid_waypoints.push(sid_waypoint, sid_lines);
                    
                });
            })
            // runway set from dropdown TODO
            // same for arrival runway and airfield
            //set_arrival_airfield(data[0].arrival)
            // plot STAR
            if (window.star_waypoints && window.star_waypoints.length > 0) {
                window.star_waypoints.forEach(marker => map.removeLayer(marker));
            }
            
            // Reset the marker array
            window.star_waypoints = [];
            
            fetch("/send_star_data", {
                method: "POST",
                headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
                body: JSON.stringify({selected_star: {send_str: data[0].STAR}, arrival_airfield: {send_str: data[0].arrival}, arrival_runway: {send_str: data[0].arrival_rwy}}), 
            })
        
            .then(response => response.json())
            .then(data => {
             
                console.log(data)
                if (data.selected_star_data.length > 0){ // only do this when there is STARs
                    data.selected_star_data.sort((a, b) => a.sequence_number - b.sequence_number);
                    star_init_point = data.selected_star_data[0]; // access first STAR point
                    console.log(star_init_point)
                }
                else { // if there is no star data
                    fetch("/return_arrival_airport", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
                        body: JSON.stringify({send_str: arrivalfield}), // send airport name as the body
                    })
                    
                    .then(response => response.json())
                    .then(data => {
                        star_init_point = {
                            lat: data.arrival_latlng[0].lat,
                            lng: data.arrival_latlng[0].lng
                        };
                        display_waypoints(); // needs to be called here too, else lines arent drawn
                    })
                }

                data.selected_star_data.forEach(point => {
                    let star_waypoint = L.marker([point.lat, point.lng])
                        .bindPopup(`<b>${point.ident}</b>`)
                        .addTo(map);
                    let star_lines = L.polyline(data.selected_star_data, { color: "red"}).addTo(map);
                    if (previousPoint) {
                        distance += L.latLng(point.lat, point.lng).distanceTo(L.latLng(previousPoint.lat, previousPoint.lng));
                    }
                
                    previousPoint = point;
                    window.star_waypoints.push(star_waypoint, star_lines)});
            
            })
            // display waypoints
            selected_waypoints = "";
            selected_waypoints = data[0].waypoints;
            display_waypoints();

        })
    }
    
    // Handle "Delete Route" button click
    if (event.target.classList.contains("delete-route-btn")) {
        const routeId = event.target.getAttribute("data-route-id");
        console.log("Deleting route with ID:", routeId);
        // Disable the delete button to prevent multiple clicks
        event.target.disabled = true;
        event.target.innerText = "Deleting...";  // Change text to indicate action

        fetch("/remove_route", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                routenumber: { send_str: routeId },
                username: { send_str: localStorage.getItem("username") }
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Route removed.");
            display_user_routes();
            console.log("Routes updated");

            // Re-enable the button after the request is complete
            event.target.disabled = false;
            event.target.innerText = "Delete";  // Reset button text
        })
        .catch(error => {
            // Handle any errors in the fetch process
            console.error("Error removing route:", error);

            // Re-enable the button in case of error
            event.target.disabled = false;
            event.target.innerText = "Delete";
        });
    }
});


document.getElementById("custom_waypoint").addEventListener("click", function () {
    document.getElementById("map").style.cursor = "crosshair";

    // Wait for user to click the map
    map.once("click", function (e) {
        // Set lat/lng into the form fields
        document.getElementById("customWaypointBox").style.display = "block";
        document.getElementById("ctmwaypointLat").value = e.latlng.lat.toFixed(6);
        document.getElementById("ctmwaypointLong").value = e.latlng.lng.toFixed(6);

        // Attach the submit event only once
        const form = document.getElementById("customWaypointForm");
        const saveBtn = document.getElementById("saveCustomWaypoint");

        // Remove previous listener if it exists
        const newForm = form.cloneNode(true);
        form.parentNode.replaceChild(newForm, form);

        newForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const name = document.getElementById("ctmwaypointName").value;
            const type = document.getElementById("waypointType").value;
            const lat = parseFloat(document.getElementById("ctmwaypointLat").value).toFixed(6);
            const lng = parseFloat(document.getElementById("ctmwaypointLong").value).toFixed(6);
            const notes = document.getElementById("waypointNotes").value;

            const customwaypoint = L.marker([lat, lng])
                .bindPopup(
                    `<b>${name}</b><br>` +
                    `<i>${type}</i><br>` +
                    `<b>Lat:</b> ${lat}<br>` +
                    `<b>Lng:</b> ${lng}<br>` +
                    (notes ? `<b>Notes:</b> ${notes}` : "")
                )
                .addTo(map);

            custom_waypoint_store.push({ name, lat: parseFloat(lat), lng: parseFloat(lng), notes: notes, usage: type });

            selected_waypoints.push(name);

            display_waypoints();

            // Hide the form and reset
            document.getElementById("customWaypointBox").style.display = "none";
            newForm.reset();
        });
    });

    // Reset cursor
    map.once("click", () => {
        document.getElementById("map").style.cursor = "auto";
    });
});


document.getElementById("cancelCustomWaypoint").addEventListener("click", function(){

    document.getElementById("customWaypointBox").style.display = "none";

})