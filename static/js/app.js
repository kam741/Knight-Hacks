let map;
let geocoder;
let userLocation = null; // Will hold the user's current location
let currentRoutes = []; // To store the polylines for multiple routes

function initMap() {
    // Initialize the map at a default location while waiting for geolocation
    const defaultLocation = { lat: 39.8283, lng: -98.5795 }; // Center of the US
    map = new google.maps.Map(document.getElementById('map'), {
        center: defaultLocation,
        zoom: 5,
    });

    geocoder = new google.maps.Geocoder(); // Initialize the geocoder

    // Get the user's current location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };

                // Center the map on the user's location
                map.setCenter(userLocation);
                map.setZoom(14);

                // Add a marker to show the user's current location
                new google.maps.Marker({
                    position: userLocation,
                    map: map,
                    title: 'Your Location',
                });
            },
            function () {
                alert('Failed to retrieve your location.');
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }

    // Search button functionality
    document.getElementById('search-button').addEventListener('click', function () {
        let infoBox = document.getElementById('info-box');
        infoBox.innerHTML = '';
        if (userLocation) {
            geocodeAddressAndDrawRoute(userLocation);
        } else {
            alert("Your current location is not available yet.");
        }
    });
}

function geocodeAddressAndDrawRoute(startLocation) {
    const address = document.getElementById('address-input').value;

    // Geocode the address to get its latitude and longitude
    geocoder.geocode({ address: address }, function (results, status) {
        if (status === 'OK') {
            const destinationLocation = results[0].geometry.location;

            // Center the map at the searched location
            map.setCenter(destinationLocation);
            map.setZoom(14);

            // Call the drawCustomRoute function with both the user and the destination location
            drawCustomRoute(startLocation, destinationLocation);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function convertSecondsToHoursAndMinutes(timeSeconds) {
    // Calculate hours and minutes
    const hours = Math.floor(timeSeconds / 3600);
    const minutes = Math.floor((timeSeconds % 3600) / 60);
    
    // Create a formatted string
    return `${hours} hour(s) and ${minutes} minute(s)`;
}

function drawCustomRoute(startLocation, endLocation) {
    // Define colors for the routes
    const colors = ['#FF0000', '#FFFF00', '#0000FF']; // Red, Yellow, Blue
    const offset = .0005; // Offset value to separate overlapping routes

    // Send the start and end locations to the server
    fetch('/route-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            to: endLocation,
            from: startLocation,
        })
    })
    .then(response => response.json())
    .then(data => {
        // Clear previous routes
        currentRoutes.forEach(route => route.setMap(null));
        currentRoutes = []; // Reset current routes array

        // Loop through the lines in the response object
        
        let lineCount = 0; // To track the current line number for color assignment
        const infoBox = document.getElementById('info-box');
        infoBox.innerHTML = ''; // Clear the info box
        
        for (const line in data) {
            if (data.hasOwnProperty(line)) {
                const routeData = data[line];

                // Create a new array for coordinates with an offset
                const pathOffset = routeData.coords.map(coord => ({
                    lat: coord.lat + (lineCount * offset), // Adjust latitude for separation
                    lng: coord.lng
                }));

                const routePath = new google.maps.Polyline({
                    path: pathOffset,
                    geodesic: true,
                    strokeColor: colors[lineCount % colors.length], // Assign colors in a cycle
                    strokeOpacity: 1.0,
                    strokeWeight: 4,
                });

                // Set the route path on the map
                routePath.setMap(map);
                currentRoutes.push(routePath); // Store the route

                // Display the distance and time in the info box
                infoBox.style.display = 'block'; // Show the info box
                infoBox.innerHTML += `<div>${line.toUpperCase()}:<br> Distance: ${Math.round((routeData.distanceMeters * 0.000621371) * 10) / 10} Miles <br> Time: ${convertSecondsToHoursAndMinutes(routeData.timeSeconds)}   </div>`; // Display the distance and time

                lineCount++; // Increment the line count
            }
        }
    })
    .catch(error => {
        console.error("There was an error sending the route data:", error);
    });
}
