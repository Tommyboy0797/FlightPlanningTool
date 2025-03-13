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
        windspeed: document.getElementById("wind_speed").value,
        tail_or_head: document.getElementById("tail_or_head").innerHTML,
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
        show_sids: document.getElementById("show_sids").checked
    };
    loadAirports(filters);
});

// Load initial airports with default filters
loadAirports({ small_ap: true, medium_ap: true, large_ap: true, show_sids: true, });

enter_rwy_dropdown = document.getElementById("enterRwy");
enter_sid_dropdown = document.getElementById("chooseSid");
enter_arr_runway = document.getElementById("chooseArrRw");

function set_origin_airfield(airportname){
    document.getElementById("airport_dis").innerText = airportname

    fetch("/set_origin", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({airport_name: airportname}), // send airport name as the body
    })

    fetch(`/get_runways`, {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({airport_name: airportname}), // send airport name as the body
    })

    .then(response => response.json())
    .then(data => {

        let runways_list = data.origin_runways;

        enter_rwy_dropdown.innerHTML = ""

        runways_list.forEach(runway => {
            enter_rwy_dropdown.options[enter_rwy_dropdown.options.length] = new Option(runway, runway);
        })

        document.getElementById('available_runways').textContent = data.origin_runways.join(', ');
    })
    .catch(error => console.error('Error fetching runway data:', error));
    };


    document.getElementById("enterRwy").onchange = function () {
        if (!this.value) return; // Prevent sending empty selections
            console.log(JSON.stringify({selected_runway: this.value, airport_name: document.getElementById("airport_dis").innerText}));
            fetch("/return_runway", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({runwy: {selected_runway: this.value}, origin: {airport_name: document.getElementById("airport_dis").innerText}}),
            })

            .then(response => response.json())
            .then(data => {
   
                document.getElementById('sids_display').textContent = data.sids.join(', ');

                enter_sid_dropdown.innerHTML = "";

                data.sids.forEach(sids => {
                    enter_sid_dropdown.options[enter_sid_dropdown.options.length] = new Option(sids, sids);
                })
            })
            
            fetch("/airfield_data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({origin: {airport_name: document.getElementById("airport_dis").innerText},runwy: {selected_runway: document.getElementById("enterRwy").value}}),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Error:", data.error);
                    document.getElementById("airfield_info").textContent = "No airfield or runway selected.";
                    return;
                }
        
                document.getElementById("airfield_info").innerHTML = ""; // Clear previous data
                console.log(data.runway_data);
                data.runway_data.forEach(runway => {
                    let runwayInfo = `
                        <p><strong>Length:</strong> ${runway.length} ft</p>
                        <p><strong>Width:</strong> ${runway.width} ft</p>
                        <p><strong>Heading:</strong> ${runway.hdg}°</p>
                        <p><strong>Surface:</strong> ${runway.surface}</p>
                        <hr>
                    `;
                    document.getElementById("airfield_info").innerHTML += runwayInfo;
                });
            })
            .catch(error => console.error("Error fetching runway data:", error));
    };

    document.getElementById("chooseSid").onchange = function () {

        if (window.sid_waypoints && window.sid_waypoints.length > 0) {
            window.sid_waypoints.forEach(marker => map.removeLayer(marker));
        }
        console.log(JSON.stringify({select_sid: {selected_sid: this.value}, origin: {airport_name: document.getElementById("airport_dis").innerText}, runwy: {selected_runway: document.getElementById("enterRwy").value}}))
        // Reset the marker array
        window.sid_waypoints = [];

        fetch("/return_sid", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({select_sid: {selected_sid: this.value}, origin: {airport_name: document.getElementById("airport_dis").innerText}, runwy: {selected_runway: document.getElementById("enterRwy").value}}),
        })
        
        .then(response => response.json())
        .then(data => {
            
            document.getElementById("chosen_sid").textContent = document.getElementById("chooseSid").value;

            data.selected_sid_points.sort((a, b) => a.sequence_number - b.sequence_number);
            console.log(data.selected_sid_points);
            data.selected_sid_points.forEach(point => {
                let sid_waypoint = L.marker([point.lat, point.lng])
                    .bindPopup(`<b>${point.ident}</b>`)
                    .addTo(map);
                let sid_lines = L.polyline(data.selected_sid_points, { color: "blue"}).addTo(map);
                window.sid_waypoints.push(sid_waypoint, sid_lines);
                
            });

        })
    };

let arrivalairport = ""
function set_arrival_airfield(arrival_field) {
    arrivalairport = arrival_field
    fetch("/return_arrival_airport", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({arrival_field: arrival_field}), // send airport name as the body
    })
    
    .then(response => response.json())
    .then(data => {

        enter_arr_runway.innerHTML = "";

        data.arrival_runways.forEach(runway => {
            enter_arr_runway.options[enter_arr_runway.options.length] = new Option(runway, runway);
        })
    })
}


document.getElementById("chooseArrRw").onchange = function () {

    fetch("/handle_stars", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({selected_runway: {arrival_runway: this.value},arrival_airfield: {arrival_field: arrivalairport}}), 
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

    // Reset the marker array
    window.star_waypoints = [];

    fetch("/send_star_data", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({selected_star: {selected_star: this.value}, arrival_airfield: {arrival_field: arrivalairport}, arrival_runway: {arrival_runway: document.getElementById("chooseArrRw").value}}), 
    })

    .then(response => response.json())
    .then(data => {
     
        document.getElementById("userRoute").innerHTML = data.route

        data.selected_star_data.sort((a, b) => a.sequence_number - b.sequence_number);

        data.selected_star_data.forEach(point => {
            let star_waypoint = L.marker([point.lat, point.lng])
                .bindPopup(`<b>${point.ident}</b>`)
                .addTo(map);
            let star_lines = L.polyline(data.selected_star_data, { color: "red"}).addTo(map);
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
        body: JSON.stringify({waypointname: this.value}), 
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
    fetch("/append_route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({waypoint: {waypoint: waypoint_name}, origin: {airport_name: document.getElementById("airport_dis").innerText}, runwy: {selected_runway: document.getElementById("enterRwy").value}, select_sid: {selected_sid: document.getElementById("chooseSid").value}, selected_star: {selected_star: document.getElementById("chooseArrStar").value},selected_runway: {arrival_runway: document.getElementById("chooseArrRw").value} ,arrival_airfield: {arrival_field: arrivalairport}}),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("userRoute").innerHTML = data.route;
        display_waypoints(); // Ensure waypoints are displayed after updating the route
    });
}


function display_waypoints() {
    let fetchPromises = selected_waypoints.map(wp => {
        return fetch("/waypoint_info", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ waypointname: wp }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.waypointdata.length > 0) {
                waypoint_data_values.push(data.waypointdata[0]); // Store only first waypoint object
            }
        });
    });

    // Wait for all fetches to complete before adding markers
    Promise.all(fetchPromises).then(() => {
        // Remove existing markers before adding new ones
        if (window.waypoint_markers && window.waypoint_markers.length > 0) {
            window.waypoint_markers.forEach(marker => map.removeLayer(marker));
        }
        
        // Reset marker storage
        window.waypoint_markers = [];

        // Add new markers
        waypoint_data_values.forEach(point => {
            let waypoint_marker = L.marker([point.lat, point.lng])
                .bindPopup(`<b>${point.name}<br> ${point.usage}<br>${point.icao}${point.area} 
                <br> <button onclick="remove_wp_from_route('${point.lat}, ${point.lng}')">Remove</button></b>`)
                .addTo(map);

            // Store marker so it can be cleared later
            window.waypoint_markers.push(waypoint_marker);
        });

        // Now add the polyline for the route
        if (window.routePolyline) {
            map.removeLayer(window.routePolyline);
        }
        
        let latlngs = waypoint_data_values.map(point => [point.lat, point.lng]);
        
        if (latlngs.length > 1) {
            window.routePolyline = L.polyline(latlngs, { color: "green" }).addTo(map);
        }

        console.log("Updated Route with Waypoints:", latlngs);
    });
}




document.getElementById("enter_wind_box").onchange = function () {
    stringified_wind_hdg = JSON.stringify({windhdg: this.value})

    fetch("/handle_winds", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: JSON.stringify({windhdg: {windhdg: this.value}, origin: {airport_name: document.getElementById("airport_dis").innerText}, runwy: {selected_runway: document.getElementById("enterRwy").value}}), 
    })
    .then(response => response.json())
    .then(data => {
        
        document.getElementById("tail_or_head").innerHTML = data.head_or_tail_wind

        
    })
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
        body: JSON.stringify({airway_value: this.value})
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