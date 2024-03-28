from data_vars import line_station_map

import pandas as pd
from dbfread import DBF
import numpy as np
import requests
import time
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Define file path to the DBF file
file_path = './data/metro.dbf'

# Read the DBF file into a DataFrame
table = DBF(file_path, load=True)
df = pd.DataFrame(iter(table))

# Extract relevant columns and explode 'LINE' column
df_shorten = df[['NAME', 'LINE']]
df['LINE'] = df['LINE'].str.split(r',\s*')
df_exploded = df.explode('LINE').reset_index(drop=True)

# Function to get latitude and longitude from address
def get_lat_lon(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}
    response = requests.get(url, params=params)
    if response.json():
        data = response.json()[0]
        return float(data['lat']), float(data['lon'])
    else:
        return None, None

# Add 'Latitude' and 'Longitude' columns to DataFrame
print('Downloading data...')
for index, row in df_exploded.iterrows():
    lat, lon = get_lat_lon(row['ADDRESS'])
    df_exploded.at[index, 'Latitude'] = lat
    df_exploded.at[index, 'Longitude'] = lon
    time.sleep(1)  # Sleep to respect usage policy
print('Done downloading!')

# Create GeoDataFrame with coordinates
gdf = gpd.GeoDataFrame(df_exploded, geometry=gpd.points_from_xy(df_exploded.Longitude, df_exploded.Latitude))

# Load a map of the world for background
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
usa = world[world.name == "United States of America"]

# Define line colors
line_colors = {'blue': 'blue', 'orange': 'orange', 'silver': '#C0C0C0', 'red': 'red', 'green': 'green', 'yellow': 'yellow'}

# Clean and process data
initial_row_count = len(df_exploded)
df_exploded_cleaned = df_exploded.dropna(subset=['ADDRESS', 'LINE'])
final_row_count = len(df_exploded_cleaned)
rows_removed = initial_row_count - final_row_count

# Generate random visitor counts
np.random.seed(42)
df_exploded_cleaned['VISITORS'] = np.random.lognormal(mean=np.log(10000), sigma=1, size=final_row_count)
df_exploded_cleaned['VISITORS'] = df_exploded_cleaned['VISITORS'].round().astype(int)

# Drop duplicates and save to CSV
df_exploded_unique = df_exploded_cleaned.drop_duplicates(subset=['LINE', 'Longitude', 'Latitude'])
df_exploded_unique.to_csv('visitors_Metrostations.csv', index=False)


# Load data from CSV
data = pd.read_csv("visitors_Metrostations.csv")
data['geometry'] = data.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)

# Group data by station name, line color, and visitors
grouped_data = data.groupby(['NAME', 'LINE', 'VISITORS'])['geometry'].apply(list).reset_index()

for index, row in grouped_data.iterrows():
    station_name = row['NAME']
    line_color = row['LINE']
    visitors = row['VISITORS']
    points = row['geometry']
    # Check if there are at least two valid points
    valid_points = [point for point in points if not point.is_empty]
    if len(valid_points) > 1:
        # Extract coordinates as tuples (x, y)
        coordinates = [(point.x, point.y) for point in valid_points]

# Plot metro lines
fig, ax = plt.subplots(figsize=(10, 10))
ordered_lines = []

# Iterate over station lists to plot lines
for line, stations in line_station_map.items():
    ordered_lines.append((line, stations))
    station_coordinates = {}
    
    # Retrieve station coordinates
    for station in stations:
        station_data = df_exploded_unique[df_exploded_unique['NAME'] == station]
        if not station_data.empty:
            station_coordinates[station] = (station_data.iloc[0]['Longitude'], station_data.iloc[0]['Latitude'])
    
    # Sort stations and plot
    sorted_stations = [(station, station_coordinates[station]) for station in stations if station in station_coordinates]
    for station, coordinates in sorted_stations:
        ax.scatter(coordinates[0], coordinates[1], color=line_colors[line], s=visitors/100)
        ax.text(coordinates[0], coordinates[1], station, fontsize=8, ha='right', va='center', color='black')
    
    # Connect points with lines
    station_coordinates = [station[1] for station in sorted_stations]
    ax.plot([coord[0] for coord in station_coordinates], [coord[1] for coord in station_coordinates], color=line_colors[line], linewidth=2, label=line.capitalize() + " Line")

plt.title('Metro Map with Connected Stations (Ordered)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()
