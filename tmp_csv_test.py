from chatbot import parse_request
from traffic_predictor import predict_traffic
from road_graph import create_graph, update_graph_weights, get_edge_info
from routing import find_shortest_path

print('Graph creation...')
G = create_graph()
print('Nodes:', len(G.nodes), 'Edges:', len(G.edges))
print('Edge info Chennai->Kanchipuram:', get_edge_info(G, 'Chennai', 'Kanchipuram'))

intent = parse_request('Best route from Chennai to Kanchipuram at 8am')
print('Intent:', intent)

traffic = predict_traffic(intent['source'], intent['destination'], intent['time'])
print('Traffic pred', traffic)

G = update_graph_weights(G, traffic)
path, travel_time = find_shortest_path(G, intent['source'], intent['destination'])
print('Path', path, 'time', travel_time)
