import networkx as nx


def find_shortest_path(G, source, destination):
    # preserve node names as they are in graph (case-sensitive as in CSV)
    if source not in G.nodes or destination not in G.nodes:
        # try title-case fallback for nicer display
        source = source.title()
        destination = destination.title()
        if source not in G.nodes or destination not in G.nodes:
            return None, None

    try:
        path = nx.dijkstra_path(G, source, destination, weight='weight')
        travel_time = nx.dijkstra_path_length(G, source, destination, weight='weight')
    except nx.NetworkXNoPath:
        return None, None

    return path, int(travel_time)
