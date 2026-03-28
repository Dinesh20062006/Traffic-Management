from chatbot import parse_request
from traffic_predictor import predict_traffic
from road_graph import create_graph, update_graph_weights
from routing import find_shortest_path

print(parse_request('Best route from A to D at 6pm'))
print(parse_request('Traffic at 9am'))
print(parse_request('Route from B to E'))
print(parse_request('A to D'))
print(parse_request('6pm'))

G=create_graph()
traffic=predict_traffic('A','D','6pm')
update_graph_weights(G,traffic)
path,time=find_shortest_path(G,'A','D')
print(path,time)
