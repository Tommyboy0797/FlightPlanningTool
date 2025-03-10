
waypoints = []  # Store multiple waypoints

def add_waypoint(waypoint):
    waypoints.append(waypoint)

def build_route(origin_airfield, selected_runway,selected_sid,selected_star,selected_runway_arrival,arrival_airfield):
    route_parts = []
    waypoints = [] 
    route = ""
    
    if origin_airfield:
        route_parts.append(origin_airfield)
        if selected_runway:
            route_parts.append(selected_runway)
        if selected_sid:
            route_parts.append(selected_sid)

    if waypoints:
        route_parts.extend(waypoints)

    if selected_star:
        route_parts.append(selected_star)
    if selected_runway_arrival:
        route_parts.append(selected_runway_arrival)
    if arrival_airfield:
        route_parts.append(arrival_airfield)

    route = " -> ".join(route_parts)
    return route
