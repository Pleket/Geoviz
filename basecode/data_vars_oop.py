from Station import Station
from Line import Line, MetroLine
from data_vars import line_station_map
from step1 import df_exploded_unique

def get_station_data(line_station_map, df_exploded_unique):
    station_lines = {}
    stations = []

    for line, line_stations in line_station_map.items():
        for st in line_stations:
            station_coords = df_exploded_unique[df_exploded_unique['NAME'] == st]
            if not station_coords.empty:
                if st not in station_lines:
                    station_lines[st] = [line]
                else:
                    station_lines[st].append(line)
                stations.append(Station(st, station_coords.iloc[0]['Longitude'], station_coords.iloc[0]['Latitude']))
                stations[-1].set_lines(station_lines[st])
            else:
                print(f"Station {st} not found in the dataset. Skipping...")

    print("Populated Stations:")
    for station in stations:
        print(f"Name: {station.get_name()}, Lines: {station.get_lines()}, Coordinates: {station.get_coordinates()}")

    station_dict = {station.get_name(): station for station in stations}

    return stations, station_dict


def get_line_data(line_station_map):
    lines = []

    stations, stations_dict = get_station_data(line_station_map, df_exploded_unique)

    for color, stations in line_station_map.items():
        metro_line = MetroLine(color)
        for i in range(len(stations) - 1):
            station1 = stations_dict.get(stations[i])
            station2 = stations_dict.get(stations[i+1])
            if station1 and station2:  # Check if both stations are found
                line = Line(color, station1, station2)
                metro_line.add_line(line)
        lines.append(metro_line)

    return lines


get_line_data(line_station_map)
