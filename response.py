def format_route_response(source, destination, query_time, path, travel_time, traffic_pred):
    if not path:
        return f"No route found from {source} to {destination}."

    path_str = ' → '.join(path)
    level = traffic_pred.get('level', 'Unknown')
    return (f"At {query_time}, traffic level between {source} and {destination} is {level}. "
            f"Recommended route: {path_str}. Estimated travel time: {travel_time} min.")


def format_traffic_response(target, query_time, traffic_pred):
    level = traffic_pred.get('level', 'Unknown')
    desc = traffic_pred.get('description', '')
    return (f"Traffic forecast for {target} at {query_time}: {level}. {desc}")
