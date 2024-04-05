import math
import numpy as np
import matplotlib.pyplot as plt
from step1 import line_station_map, df_exploded_unique, visitors
from data_vars import line_colors
from Station import Station
from Line import Line

# Compute a list of stations with their corresponding lines
def get_station_data(line_station_map, df_exploded_unique):
    station_lines = {}
    for line, line_stations in line_station_map.items():
        for st in line_stations:
            if st not in station_lines:
                station_lines[st] = [line]
            else:
                station_lines[st].append(line)

    stations = []        
    for st in station_lines:
        station_coords = df_exploded_unique[df_exploded_unique['NAME'] == st]

        if not station_coords.empty:
            stations.append(Station(st, station_coords.iloc[0]['Longitude'], station_coords.iloc[0]['Latitude']))
            stations[-1].set_lines(station_lines[st])
        else:
            print(f"Station {st} not found in the dataset")
    
    return stations

# Pick a center station from a list of stations
def pick_center(stations):
    num_dists = []
    avg_dists = []

    weighted_center = (0,0)
    station_line_pairs = 0

    for i in range(len(stations)):
        num_dists.append(0)
        avg_dists.append(0)

        new_weights = tuple(z * len(stations[i].get_lines()) for z in stations[i].get_coordinates())
        weighted_center = tuple(map(sum, zip(weighted_center, new_weights)))

        station_line_pairs += len(stations[i].get_lines())
    
    weighted_center = tuple(x / station_line_pairs for x in weighted_center)

    min_dist = 10000000
    weighted_min_station = None
    for i in range(len(stations)):
        dist = math.sqrt((weighted_center[0] - stations[i].get_coordinates()[0])**2 + (weighted_center[1] - stations[i].get_coordinates()[1])**2)
        if dist < min_dist:
            min_dist = dist
            weighted_min_station = stations[i]

    return weighted_min_station

    # for i in range(len(stations)):
    #     for j in range(len(stations)):
    #         if i != j:


    #             num_dists[i] += 1
    #             avg_dists[i] += math.sqrt((stations[i][0] - stations[j][0])**2 + (stations[i][1] - stations[j][1])**2)

pick_center(get_station_data(line_station_map, df_exploded_unique))