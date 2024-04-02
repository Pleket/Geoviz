# Import necessary functions from draw.py and step2.py
from metromap_drawing.draw import draw_lines, draw_rectangle_station
from step2 import line_station_map, df_exploded_unique, visitors, snap_to_grid, grid_size
from data_vars import line_colors, station_lines
import math
import numpy as np
import drawsvg as draw

# Create a list to store the ordered lines
ordered_lines = []

# Create a list to store all coordinates
all_coordinates = []

# Iterate over the provided station lists and append the line name to ordered_lines
for line_color, stations in line_station_map.items():
    ordered_lines.append((line_color, stations))
    for station in stations:
        station_data = df_exploded_unique[df_exploded_unique['NAME'] == station]
        if not station_data.empty:
            all_coordinates.append((station_data.iloc[0]['Longitude'], station_data.iloc[0]['Latitude']))

# Find the minimum and maximum coordinates
min_coor = np.nanmin(all_coordinates, axis=0)
max_coor = np.nanmax(all_coordinates, axis=0)

# Determine the scaling factor based on the ratio between the drawing size and the grid size
scaling_factor = 300 // grid_size - 1  # Assuming 300 is the size of the drawing

# Create SVG drawing
dr = draw.Drawing(300, 300, origin='top-left')

# # Draw metro lines
for line_color, stations in ordered_lines:
    station_coordinates = []
    for station_name in stations:  
        station_data = df_exploded_unique[df_exploded_unique['NAME'] == station_name]  
        if not station_data.empty:
            station_coordinates.append((station_data.iloc[0]['Longitude'], station_data.iloc[0]['Latitude']))
    
    # Scale up and snap the coordinates to the grid
    snapped_stations = [snap_to_grid((x , y), min_coor, max_coor) for x, y in station_coordinates]
    scaled_stations = [(x * scaling_factor, y * scaling_factor) for x, y in snapped_stations]

    # Draw the lines
    for i in range(len(scaled_stations) - 1):
        station_curr = scaled_stations[i]
        station_next = scaled_stations[i + 1]
        num_lines_curr = len(station_lines.get(station_curr, []))
        num_lines_next = len(station_lines.get(station_next, []))
        lines = max(num_lines_curr, num_lines_next)
        color = line_colors[line_color]
        if station_curr[0] < station_next[0]:
            if station_next[0] - station_curr[0] == 0:
                rotate = 90
            else:
                rotate = math.degrees(math.atan((station_next[1] - station_curr[1]) / (station_next[0] - station_curr[0])))
        elif station_curr[0] > station_next[0]:
            if station_next[0] - station_curr[0] == 0:
                rotate = -90
            else:
                rotate = math.degrees(math.atan((station_next[1] - station_curr[1]) / (station_next[0] - station_curr[0])))
        else:
            rotate = 0
        print(int(station_curr[0]+5), int(station_curr[1]+5), int(station_next[0]+5), int(station_next[1]+5), lines, dr, 2, color, rotate)
        draw_lines(int(station_curr[0]+5), int(station_curr[1]+5), int(station_next[0]+5), int(station_next[1]+5), 1, dr, 2, [color], rotate)






# Draw metro stations
for line_color, stations in ordered_lines:
    station_coordinates = []
    for station_name in stations:
        station_data = df_exploded_unique[df_exploded_unique['NAME'] == station_name]
        if not station_data.empty:
            station_coordinates.append((station_data.iloc[0]['Longitude'], station_data.iloc[0]['Latitude']))
    
    # Scale up and snap the coordinates to the grid
    snapped_stations = [snap_to_grid((x , y), min_coor, max_coor) for x, y in station_coordinates]
    scaled_stations = [(x * scaling_factor, y * scaling_factor) for x, y in snapped_stations]

    # Draw the stations
    for coordinates in scaled_stations:
        num_lines = len(line_colors)
        #TODO: Fix the lines_h and lines_v
        lines_h = num_lines
        lines_v = num_lines
        color = line_colors[line_color]
        # print('Stations: ',coordinates[0], coordinates[1], lines_h, lines_v, dr)
        draw_rectangle_station(coordinates[0]+5, coordinates[1]+5, lines_h, lines_v, dr, line_thickness=2, color=color)

# Set pixel scale and save SVG
dr.set_pixel_scale(5)
dr.save_svg('metro_map.svg')
