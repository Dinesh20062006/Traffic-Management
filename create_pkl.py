import pandas as pd
import pickle

# Load the CSV data
df = pd.read_csv('tamil_nadu_traffic_data.csv')

# Convert to a dictionary for easy access: key = (source, target), value = dict of data
data_dict = {}
for _, row in df.iterrows():
    key = (row['source'], row['target'])
    data_dict[key] = {
        'base_time': row['base_time'],
        'low_traffic_factor': row['low_traffic_factor'],
        'medium_traffic_factor': row['medium_traffic_factor'],
        'high_traffic_factor': row['high_traffic_factor'],
        'example_hour': row['example_hour'],
        'traffic_level': row['traffic_level'],
        'predicted_time': row['predicted_time']
    }

# Save to PKL file
with open('tamil_nadu_traffic_data.pkl', 'wb') as f:
    pickle.dump(data_dict, f)

print("PKL file created successfully.")