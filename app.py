from flask import Flask, render_template, request
from chatbot import parse_request
from traffic_predictor import predict_traffic, _load_traffic_csv
from road_graph import create_graph, update_graph_weights
from routing import find_shortest_path
from response import format_route_response, format_traffic_response

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    error = None
    route_data = None
    all_routes = _load_traffic_csv()

    if request.method == 'POST':
        user_text = request.form.get('user_text', '').strip()
        source = request.form.get('source', '').strip()
        destination = request.form.get('destination', '').strip()
        time_str = request.form.get('time', '').strip()

        if not user_text:
            # If user typed no sentence, allow explicit source/destination/time fields still
            if source and destination:
                intent = {
                    'type': 'route',
                    'source': source,
                    'destination': destination,
                    'time': time_str or 'now'
                }
            elif time_str:
                intent = {
                    'type': 'traffic',
                    'source': None,
                    'destination': None,
                    'time': time_str
                }
            else:
                error = 'Please enter a question or request.'
                intent = None
        else:
            intent = parse_request(user_text)
            intent['source'] = (source or intent.get('source') or '').title()
            intent['destination'] = (destination or intent.get('destination') or '').title()
            intent['time'] = time_str or intent.get('time', 'now')

        if intent and not error:
            if intent['type'] == 'route':
                source = intent.get('source')
                destination = intent.get('destination')
                query_time = intent.get('time', 'now')

                if not source or not destination:
                    error = 'Route requests require source and destination.'
                else:
                    graph = create_graph()
                    traffic_pred = predict_traffic(source, destination, query_time)
                    update_graph_weights(graph, traffic_pred)
                    path, travel_time = find_shortest_path(graph, source, destination)
                    response = format_route_response(source, destination, query_time, path, travel_time, traffic_pred)
                    route_data = {
                        'path': path,
                        'travel_time': travel_time,
                        'traffic_level': traffic_pred.get('level', 'Unknown'),
                        'source': source,
                        'destination': destination,
                        'query_time': query_time
                    }

            elif intent['type'] == 'traffic':
                target = source or destination or intent.get('source') or intent.get('destination') or 'road network'
                query_time = intent.get('time', 'now')
                traffic_pred = predict_traffic(target, target, query_time)
                response = format_traffic_response(target, query_time, traffic_pred)

            else:
                error = 'Sorry, I did not understand the question. Try "Best route from A to B" or "Traffic at 6 PM".'

    return render_template('index.html', response=response, error=error, route_data=route_data, all_routes=all_routes)

@app.route('/database')
def database():
    from traffic_predictor import _load_traffic_csv
    all_routes = _load_traffic_csv()
    return render_template('database.html', all_routes=all_routes)

if __name__ == '__main__':
    app.run(debug=True)
