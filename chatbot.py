import re


def parse_request(text):
    text_low = text.lower().strip()
    route_pattern = r'(?:from\s+)?(?P<source>[A-Za-z0-9]+)\s*(?:to|->|-|\u2192)\s*(?P<destination>[A-Za-z0-9]+)'
    time_pattern = r'(?:at|@)\s*(?P<time>[0-9]{1,2}(?::[0-9]{2})?\s*(?:am|pm)?)'

    source = None
    destination = None
    query_time = None

    route_match = re.search(route_pattern, text_low)
    if route_match:
        source = route_match.group('source').title()
        destination = route_match.group('destination').title()

    time_match = re.search(time_pattern, text_low)
    if time_match:
        query_time = time_match.group('time')

    if 'route' in text_low or route_match:
        return {
            'type': 'route',
            'source': source,
            'destination': destination,
            'time': query_time or 'now'
        }

    if 'traffic' in text_low or 'congestion' in text_low or time_match:
        return {
            'type': 'traffic',
            'source': source,
            'destination': destination,
            'time': query_time or 'now'
        }

    return {
        'type': 'unknown',
        'source': source,
        'destination': destination,
        'time': query_time or 'now'
    }
