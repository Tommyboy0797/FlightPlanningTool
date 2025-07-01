# Flight Planning Tool

A quick site that can be used to plan flights. 


## Deployment

### Building
To build locally, ensure that you have podman installed [https://podman-desktop.io/downloads] and WSL if running Windows.

To build and run the application, execute ./scripts/build_and_run_local_dev.ps1 from a terminal. This will build the container, and start the application with port 8000 forwarded. You can then access the application locally at `127.0.0.1:8000`.

### Deployment
This project uses with `GCP/GCR` to build containers, and is deployed `GKE` programatically via `Cloud Build integration`.

Deployments to dev (`flightplanning-dev.airplanesimulations.com`) are triggered by commits to the `dev` branch.

Deployments to prod are triggered by commits to `main`.

The development workflow should generally be `feature-branch` -> `dev` -> `main`.


## Features

- GPS waypoints
- Airways
- SIDs/STARs
- Custom route points
- Custom threat rings with preset SAM profiles
- Range rings -> *(currently based on the C-130J-30)*
- Aiports, airfields, airstrips
- Airport, airfield, airstrip, waypoint, airway, search boxes/viewer
- Nearby waypoints function
- Login/Signup and profile
- Save route to profile, and load from profile
- Takeoff and Landing Data (TOLD) calculator including:
    - Rotation speed
    - Refusal speed
    - Takeoff distance
    - More WIP...
- Weather page for arrival airfield and departure airfield including:
    - Raw METAR
    - Wind
    - Clouds
    - Visibility
    - Dewpoint
    - Humidity
    - Temperature
    - Altimeter -> *(converts automatically between inHg and hPa depending on source)*
    - Remarks
    - METAR time

## Roadmap

- Export flight plans to MSFS and DCS

- Link DCS and display data

- More weather options, such as enroute

- Aditional profile features such as PFP

- Collaborative editing of flight plans

- Save PPTs and custom route points

# LICENSE

This project is not open source.
The code is provided for educational and reference purposes only.
Do not copy, modify, distribute, or use it in any form without express permission.

