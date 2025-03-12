
podman build -t flightplanning:local . ;
podman run -p 8000:8000 flightplanning:local;
