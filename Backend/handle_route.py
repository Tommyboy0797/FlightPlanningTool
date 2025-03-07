origin_airfield = ""
route = ""
selected_runway = ""
selected_sid = ""
arrival_airfield = ""
selected_runway_arrival = ""
selected_star = ""
runway_slope = ""
waypoints = []  # Store multiple waypoints

def add_waypoint(waypoint):
    """Adds a waypoint to the list in order."""
    global waypoints
    waypoints.append(waypoint)

def build_route():
    """Constructs the route dynamically based on the user's inputs."""
    route_parts = []
    
    # Add origin details
    if origin_airfield:
        route_parts.append(origin_airfield)
        if selected_runway:
            route_parts.append(selected_runway)
        if selected_sid:
            route_parts.append(selected_sid)
    
    # Add waypoints if available
    if waypoints:
        route_parts.extend(waypoints)
    
    # Add arrival details
    if selected_star:
        route_parts.append(selected_star)
    if selected_runway_arrival:
        route_parts.append(selected_runway_arrival)
    if arrival_airfield:
        route_parts.append(arrival_airfield)
    
    # Join everything with "->" and update route
    global route
    route = " -> ".join(route_parts)
