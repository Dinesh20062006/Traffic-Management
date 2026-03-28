import csv
import os
import networkx as nx


def _load_traffic_csv():
    csv_path = os.path.join(os.path.dirname(__file__), 'tamil_nadu_traffic_data.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Traffic CSV not found: {csv_path}")

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def create_graph():
    G = nx.DiGraph()

    for row in _load_traffic_csv():
        src = row['source'].strip()
        dst = row['target'].strip()
        base_time = float(row.get('base_time', 0) or 0)
        low_factor = float(row.get('low_traffic_factor', 1.0) or 1.0)
        medium_factor = float(row.get('medium_traffic_factor', 1.2) or 1.2)
        high_factor = float(row.get('high_traffic_factor', 1.5) or 1.5)

        G.add_edge(src, dst, base_time=base_time,
                   low_factor=low_factor,
                   medium_factor=medium_factor,
                   high_factor=high_factor,
                   traffic_level=row.get('traffic_level', '').lower())

    for u, v, d in G.edges(data=True):
        d['weight'] = d.get('base_time', 1)

    return G


def update_graph_weights(G, traffic_prediction):
    # Apply overall network factor (e.g., direct traffic query)
    factor = traffic_prediction.get('factor', 1.0)

    for u, v, d in G.edges(data=True):
        d['weight'] = d.get('base_time', 1) * factor

    return G


def get_edge_info(G, source, destination):
    if G.has_edge(source, destination):
        return G.edges[source, destination]
    return None
