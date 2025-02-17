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

document.getElementById('dataForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        gwt: document.getElementById('gwt').value,
        get_to_factor: document.getElementById('get_to_factor').value,
        get_rwy_available: document.getElementById('get_rwy_available').value,
        get_rwy_slope: document.getElementById('get_rwy_slope').value,
        enter_db_country: document.getElementById('enter_db_country').value
    };
    
    const params = new URLSearchParams(formData);
    
    fetch(`/get_data?${params}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('gross_weight_txt').textContent = `${data.gross_weight_text} lbs`;
            document.getElementById('takeofffactortext').textContent = data.takeoff_factor_text;
            document.getElementById('runway_avail_text').textContent = `${data.runway_avail} feet`;
            document.getElementById('runway_slope_text').textContent = `${data.runway_slope} degrees`;
            document.getElementById('uncorrected_max_eff_TO_dist_text').textContent = `${data.uncorrected_max_eff_TO_dist} feet`;
            document.getElementById('rotation_speed_calculated_text').textContent = `${data.rotation_speed_calculated} knots`;
            document.getElementById('uncorrected_refusal_test_p2_text').textContent = `${data.uncorrected_refusal_test_p2} knots`;
            document.getElementById('partially_corrected_refusal_p3_text').textContent = data.partially_corrected_refusal_p3;
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
                <b>${airport.name}</b> (${airport.type})<br>
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
enter_sid_dropdown = document.getElementById("chooseSid")

function set_origin_airfield(airportname){
    var stringified_origin = JSON.stringify({airport_name: airportname}) // airportname is now a JSON format
    console.log(stringified_origin)

    document.getElementById("userRoute").innerHTML = airportname // setting the text for userroute to the origin for the route

    fetch("/set_origin", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: stringified_origin, // send airport name as the body
    })

    const dropdown = document.getElementById("runways_dropdown");


    fetch(`/get_runways?`)
    .then(response => response.json())
    .then(data => {

        let runways_list = data.origin_runways;

        enter_rwy_dropdown.innerHTML = ""

        runways_list.forEach(runway => {
            enter_rwy_dropdown.options[enter_rwy_dropdown.options.length] = new Option(runway, runway);
        })

        document.getElementById('available_runways').textContent = data.origin_runways.join(', ');
    })
    
    }


    document.getElementById("enterRwy").onchange = function () {
        // set_origin_airfield(airport_name_is)
        let selected_rwy = this.value;
        if (!selected_rwy) return; // Prevent sending empty selections

            let stringified_selected_runway = JSON.stringify({selected_runway: selected_rwy});

            fetch("/return_runway", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: stringified_selected_runway,
            })

            .then(response => response.json())
            .then(data => {
   
                document.getElementById('sids_display').textContent = data.sids.join(', ');

                console.log(data.sids);

                enter_sid_dropdown.innerHTML = ""

                data.sids.forEach(sids => {
                    enter_sid_dropdown.options[enter_sid_dropdown.options.length] = new Option(sids, sids);
                })

            })
            .catch(error => console.error("Error sending selected runway:", error));
         };

    document.getElementById("chooseSid").onchange = function () {
        let selected_sid = this.value;
        let stringified_selected_sid = JSON.stringify({selected_sid: selected_sid});

        if (window.sid_waypoints && window.sid_waypoints.length > 0) {
            window.sid_waypoints.forEach(marker => map.removeLayer(marker));
        }

        // Reset the marker array
        window.sid_waypoints = [];

        fetch("/return_sid", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: stringified_selected_sid,
        })

        .then(response => response.json())
        .then(data => {
            
            console.log("selected sid", data.selected_sid);
            console.log("sid points", data.selected_sid_points);

            document.getElementById("chosen_sid").textContent = data.selected_sid;

            data.selected_sid_points.sort((a, b) => a.sequence_number - b.sequence_number);

            data.selected_sid_points.forEach(point => {
                let sid_waypoint = L.marker([point.lat, point.lng])
                    .bindPopup(`<b>${point.ident}</b>`)
                    .addTo(map);
                let sid_lines = L.polyline(data.selected_sid_points, { color: "blue"}).addTo(map);
                window.sid_waypoints.push(sid_waypoint, sid_lines);
                
            });

        })
    };
 
function set_arrival_airfield(arrival_field) {
    stringified_arrival = JSON.stringify({arrival_field: arrival_field});

    fetch("/return_arrival_airport", {
        method: "POST",
        headers: {"Content-Type": "application/json"}, //tell the server its recieving json data
        body: stringified_arrival, // send airport name as the body
    })
    
    
    .then(response => response.json())
    .then(data => {

        console.log("Selected Arrival: ", data.arrival_airfield);

    })
}