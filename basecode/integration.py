# Import necessary functions from draw.py and step2.py
from metromap_drawing.draw import draw_lines, draw_rectangle_station
from step2 import line_station_map, df_exploded_unique, visitors, snap_to_grid
from data_vars import line_colors
import math
import numpy as np


# Create a list to store the ordered lines
ordered_lines = []

# Iterate over the provided station lists and append the line name to ordered_lines
for line, stations in line_station_map.items():
    ordered_lines.append((line, stations))

# Define the size of the grid
grid_size = 10

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

# Create SVG drawing
import drawsvg as draw
dr = draw.Drawing(300, 300, origin='center')

# Draw metro lines and stations
for line_color, stations in ordered_lines:
    station_coordinates = []
    for station in stations:
        station_data = df_exploded_unique[df_exploded_unique['NAME'] == station]
        if not station_data.empty:
            station_coordinates.append((station_data.iloc[0]['Longitude'], station_data.iloc[0]['Latitude']))

    # Sort the stations based on their order in the provided list
    sorted_stations = sorted(station_coordinates, key=lambda x: stations.index(df_exploded_unique[df_exploded_unique['Longitude'] == x[0]]['NAME'].values[0]))

    # Plot stations and their names next to the points, snapped to the grid
    for index, coordinates in enumerate(sorted_stations):
        if not any(math.isnan(coord) for coord in coordinates):
            snapped_coordinates = snap_to_grid(coordinates, min_coor, max_coor)
            draw_rectangle_station(snapped_coordinates[0], snapped_coordinates[1], 0, 5, dr, 2)

    # Connect points of the same color with lines
    for i in range(len(sorted_stations) - 1):
        if not any(math.isnan(coord) for coord in sorted_stations[i]) and not any(math.isnan(coord) for coord in sorted_stations[i+1]):
            draw_lines(sorted_stations[i][0], sorted_stations[i][1], sorted_stations[i+1][0], sorted_stations[i+1][1], 5, dr, 2, [line_colors[line_color]] * 5)

# Set pixel scale and save SVG
dr.set_pixel_scale(5)
dr.save_svg('metro_map.svg')
