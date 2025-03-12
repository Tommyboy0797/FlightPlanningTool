# Flight planning tool wip

Current version - Alpha testing version.


### Building
To build locally, ensure that you have podman installed[https://podman-desktop.io/downloads] and WSL if running Windows.

To build and run the application, execute `./scripts/build_and_run_local_dev.ps1` from a terminal.
This will build the container, and start the application with port 8000 forwarded.
You can then access the application locally at `127.0.0.1:8000`.


### Deployment
This project uses with GCP/GCR to build containers, and is deployed GKE programatically via Cloud Build integration.

Deployments to dev (flightplanning-dev.airplanesimulations.com) are triggered by commits to the `dev` branch.

Deployments to prod are triggered by commits to main.

The development workflow should generally be feature-branch -> dev -> main.
