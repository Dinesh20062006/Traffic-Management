import csv
import os
import re


def _parse_time(time_str):
    if not time_str or time_str.strip().lower() == 'now':
        return 18

    text = time_str.strip().lower().replace('.', '').replace(' ', '')
    import re
    m = re.match(r'(?P<h>\d{1,2})(?::(?P<m>\d{2}))?(?P<suffix>am|pm)?', text)
    if not m:
        return 18

    hour = int(m.group('h'))
    suffix = m.group('suffix')
    if suffix:
        if suffix == 'pm' and hour < 12:
            hour += 12
        if suffix == 'am' and hour == 12:
            hour = 0

    return hour


def _load_traffic_csv():
    csv_path = os.path.join(os.path.dirname(__file__), 'tamil_nadu_traffic_data.csv')
    if not os.path.exists(csv_path):
        return []

    with open(csv_path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    return rows


def _lookup_edge_traffic(source, destination):
    rows = _load_traffic_csv()
    for row in rows:
        if row['source'].strip().lower() == source.strip().lower() and row['target'].strip().lower() == destination.strip().lower():
            return row
    return None


def predict_traffic(source, destination, time_str='now'):
    hour = _parse_time(time_str)
    row = _lookup_edge_traffic(source, destination)

    if row:
        # choose factor based on hour window
        if 7 <= hour < 9 or 17 <= hour < 19:
            level = 'High'
            factor = float(row.get('high_traffic_factor', 1.5))
        elif 9 <= hour < 12 or 14 <= hour < 17:
            level = 'Medium'
            factor = float(row.get('medium_traffic_factor', 1.2))
        else:
            level = 'Low'
            factor = float(row.get('low_traffic_factor', 1.0))
    else:
        if 7 <= hour < 9 or 17 <= hour < 19:
            level = 'High'
            factor = 1.6
        elif 9 <= hour < 12 or 14 <= hour < 17:
            level = 'Medium'
            factor = 1.2
        else:
            level = 'Low'
            factor = 1.0

    description = f'{level} traffic at {time_str}'
    if row and row.get('traffic_level'):
        description = f"{row.get('traffic_level').capitalize()} traffic on {source} → {destination} at {time_str}"

    return {
        'source': source,
        'destination': destination,
        'time': time_str,
        'hour': hour,
        'level': level,
        'factor': factor,
        'description': description
    }
