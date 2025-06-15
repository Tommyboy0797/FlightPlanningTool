
podman build -t flightplanning:prod . ;
podman push flightplanning:prod us-central1-docker.pkg.dev/dcs-analytics-257714/flightplanning/flightplanning:prod;