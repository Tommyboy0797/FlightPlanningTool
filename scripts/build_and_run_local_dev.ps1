
podman build -t flightplanning:dev . ;
podman run -p 8000:8000 flightplanning:dev;
