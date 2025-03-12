
podman build -t flightplanning:latest . ;
podman push flightplanning:latest docker://gcr.io/dcs-analytics-257714/flightplanning:latest;
