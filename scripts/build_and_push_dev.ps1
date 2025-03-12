
podman build -t flightplanning:dev . ;
podman push flightplanning:dev docker://gcr.io/dcs-analytics-257714/flightplanning:dev;
