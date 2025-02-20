origin_airfield = ""
route = ""
selected_runway = ""
selected_sid = ""
arrival_airfield = ""
selected_runway_arrival = ""
selected_star = ""

def build_route(waypoints=""):
    """Constructs the route dynamically based on the user's inputs."""
    route_parts = []
    
    # Add origin details
    if origin_airfield:
        route_parts.append(origin_airfield)
        if selected_runway:
            route_parts.append(selected_runway)
        if selected_sid:
            route_parts.append(selected_sid)
    
    # Add waypoints if provided
    if waypoints:
        route_parts.append(waypoints)
    
    # Add arrival details
    if selected_star:
        route_parts.append(selected_star)
    if selected_runway_arrival:
        route_parts.append(selected_runway_arrival)
    if arrival_airfield:
        route_parts.append(arrival_airfield)
    
    # Join everything with commas and update route
    global route
    route = " -> ".join(route_parts)
