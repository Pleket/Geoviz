from Station import Station
from Line import Line, MetroLine
from data_vars import line_station_map
from step1 import df_exploded_unique

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
    # Print populated stations
            
    print("Populated Stations:")
    for station in stations:
        print(f"Name: {station.get_name()}, Lines: {station.get_lines()}, Coordinates: {station.get_coordinates()}")
    
    return stations


# Compute a list of Lines with their corresponding pairs of stations
def get_line_data(line_station_map):
    lines = []
    for color, stations in line_station_map.items():
        metro_line = MetroLine(color)
        for i in range(len(stations) - 1):
            line = Line(color, stations[i], stations[i+1])
            metro_line.add_line(line)
        lines.append(metro_line)
    
    # # Print populated lines and metro lines
    # print("Populated Lines:")
    # for metro_line in lines:
    #     print(f"Metro Line Color: {metro_line.get_color()}")
    #     for line in metro_line.get_lines():
    #         print(f"Line Color: {line.color}, Stations: {line.get_stations()}")
    
    return lines


# get_station_data(line_station_map, df_exploded_unique)
get_line_data(line_station_map)