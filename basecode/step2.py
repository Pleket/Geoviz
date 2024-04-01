import math
import numpy as np
import matplotlib.pyplot as plt
from step1 import line_station_map, df_exploded_unique, visitors

line_colors = {
    'blue': 'blue',
    'orange': 'orange',
    'silver': '#C0C0C0',  # Hex code for silver
    'red': 'red',
    'green': 'green',
    'yellow': 'yellow'
}

# Create a list to store the ordered lines
ordered_lines = []

# Iterate over the provided station lists and append the line name to ordered_lines
for line, stations in line_station_map.items():
    ordered_lines.append((line, stations))

# Define the size of the grid
grid_size = 10

def snap_to_grid(coordinate, min_coor, max_coor):
    grid_cell_size=(max_coor[0]-min_coor[0])/grid_size #coordinate here means coordinate for the whole map, not just this one
    cell_number_X=(coordinate[0]-min_coor[0])//grid_cell_size
    normalised_epsilon=((coordinate[0]-min_coor[0])%grid_cell_size)/grid_cell_size
    x=round(normalised_epsilon)+cell_number_X

    grid_cell_size=(max_coor[1]-min_coor[1])/grid_size #coordinate here means coordinate for the whole map, not just this one
    cell_number_Y=(coordinate[1]-min_coor[1])//grid_cell_size
    normalised_epsilon=((coordinate[1]-min_coor[1])%grid_cell_size)/grid_cell_size
    y=round(normalised_epsilon)+cell_number_Y

    return (x, y)

# Create a list to store all coordinates
all_coordinates = []

# Iterate over the provided station lists and append the line name to ordered_lines
for line_color, stations in line_station_map.items():
    for station in stations:
        station_data = df_exploded_unique[df_exploded_unique['NAME'] == station]
        if not station_data.empty:
            all_coordinates.append((station_data.iloc[0]['Longitude'], station_data.iloc[0]['Latitude']))

# Find the minimum and maximum coordinates
min_coor = np.nanmin(all_coordinates, axis=0)
max_coor = np.nanmax(all_coordinates, axis=0)

# Plot the metro lines
fig, ax = plt.subplots(figsize=(10, 10))

# Create a list to store the lines for the legend
legend_lines = []

# Plot stations and connect points of the same color in order
for line_color, stations in ordered_lines:
    # Create a dictionary to store the coordinates of each station
    station_coordinates = {}
    
    # Retrieve the coordinates of each station from the DataFrame
    for station in stations:
        station_data = df_exploded_unique[df_exploded_unique['NAME'] == station]
        if not station_data.empty:
            station_coordinates[station] = (station_data.iloc[0]['Longitude'], station_data.iloc[0]['Latitude'])
    
    # Sort the stations based on their order in the provided list
    sorted_stations = [(station, station_coordinates[station]) for station in stations if station in station_coordinates]
    
    # Plot stations and their names next to the points, snapped to the grid
    for index, (station, coordinates) in enumerate(sorted_stations):
        if not any(math.isnan(coord) for coord in coordinates):
            snapped_coordinates = snap_to_grid(coordinates, min_coor, max_coor)
            ax.scatter(snapped_coordinates[0], snapped_coordinates[1], color=line_colors[line_color], s=visitors/100)
            # ax.text(snapped_coordinates[0], snapped_coordinates[1], station, fontsize=8, ha='right', va='center', color='black')
            
    # Connect points of the same color with lines
    station_coordinates = [snap_to_grid(station[1], min_coor, max_coor) for index, station in enumerate(sorted_stations) if not any(math.isnan(coord) for coord in station[1])]
    line, = ax.plot([coord[0] for coord in station_coordinates], [coord[1] for coord in station_coordinates], color=line_colors[line_color], linewidth=2, label=line_color.capitalize() + " Line")
    legend_lines.append(line)

# Plot stations and their names next to the points, snapped to the grid
for index, (station, coordinates) in enumerate(sorted_stations):
    if not any(math.isnan(coord) for coord in coordinates):
        snapped_coordinates = snap_to_grid(coordinates, min_coor, max_coor)
        ax.scatter(snapped_coordinates[0], snapped_coordinates[1], color=line_colors[line_color], s=visitors/100)
        ax.text(snapped_coordinates[0], snapped_coordinates[1], station, fontsize=8, ha='right', va='center', color='black')
        # Print snapped coordinates
        print(f"Station: {station}, Snapped Coordinates: {snapped_coordinates}")


# Add legend for lines
ax.legend(handles=legend_lines)

plt.title('Metro Map with Connected Stations (Ordered)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
