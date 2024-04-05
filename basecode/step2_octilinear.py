from enum import Enum
import pyomo as pyo
import matplotlib.pyplot as plt
from data_vars_oop import get_line_data
from data_vars import line_station_map


def snap_grid(bounding_box, square_size, metroline, scaling_factor):
    # Create a dictionary to store the snapped coordinates
    lines = metroline.get_lines()

    new_coords1 = []
    new_coords2 = []
    trajectories = []

    # Iterate over the metroline stations
    for i in range(len(lines)):
        line = lines[i]

        coord1 = line.get_stations()[0].get_coordinates()
        coord2 = line.get_stations()[1].get_coordinates()

        # print(f"The coordinates are {coord1}")
        
        dist_1 = ((coord1[0] - (coord1[0] % square_size)) / square_size, (coord1[1] - (coord1[1] - square_size)) / square_size)
        dist_2 = ((coord2[0] - (coord2[0] % square_size)) / square_size, (coord2[1] - (coord2[1] - square_size)) / square_size)

        corner1 = compute_corner(square_size, coord1)
        corner2 = compute_corner(square_size, coord2)

        new_coord_1 = ((dist_1[0] + corner1.value[0]) * square_size * scaling_factor, (dist_1[1] + corner1.value[1]) * square_size * scaling_factor)
        new_coord_2 = ((dist_2[0] + corner2.value[0]) * square_size * scaling_factor, (dist_2[1] + corner2.value[1]) * square_size * scaling_factor)

        line_path = find_grid_path(new_coord_1, new_coord_2, square_size)
        
        new_coords1.append(new_coord_1)
        new_coords2.append(new_coord_2)
        trajectories.append(line_path)

    for i in range(len(lines)):
        lines[i].set_coords(trajectories[i])
        lines[i].station1.set_coordinates(new_coords1[i][0], new_coords1[i][1])
        lines[i].station2.set_coordinates(new_coords2[i][0], new_coords2[i][1])
    
    return metroline

def find_grid_path(coord1, coord2, square_size):
    # print(coord1)
    current_coord = (coord1[0], coord1[1])
    path = [(coord1[0], coord1[1])]

    while not (current_coord[0] > coord2[0] - square_size and current_coord[0] < coord2[0] + square_size and current_coord[1] > coord2[1] - square_size and current_coord[1] < coord2[1] + square_size):
        new_x = current_coord[0]
        new_y = current_coord[1]

        if current_coord[0] < coord2[0]:
            new_x = current_coord[0] + square_size
        elif current_coord[0] > coord2[0]:
            new_x = current_coord[0] - square_size
        
        if current_coord[1] < coord2[1]:
            new_y = current_coord[1] + square_size
        elif current_coord[1] > coord2[1]:
            new_y = current_coord[1] - square_size
        
        path.append((new_x, new_y))
        current_coord = (new_x, new_y)
    
    return path        

def compute_corner(square_size, coord):
    threshold = square_size / 2

    if coord[0] % square_size < threshold and coord[1] % square_size < threshold:
        return Corner.TOP_LEFT
    
    if coord[0] % square_size >= threshold and coord[1] % square_size < threshold:
        return Corner.TOP_RIGHT

    if coord[0] % square_size < threshold and coord[1] % square_size >= threshold:
        return Corner.BOTTOM_LEFT
    
    if coord[0] % square_size >= threshold and coord[1] % square_size >= threshold:
        return Corner.BOTTOM_RIGHT

class Corner(Enum):
    TOP_LEFT = (0,0)
    TOP_RIGHT = (1,0)
    BOTTOM_LEFT = (0,1)
    BOTTOM_RIGHT = (1,1)


def define_ILP(grid_size, square_size, metroline):
    model = pyo.ConcreteModel()

    station_vars = [(v, i, j) for v in metroline.get_lines().station1.get_name() for i in range(grid_size / square_size) for j in range(grid_size / square_size)]
    model.S = pyo.Set(dim=3, initialize=station_vars)

    station_edges = [(e, i, j, d) for e in metroline.get_lines().get_id() for i in range(grid_size / square_size) for j in range(grid_size / square_size) for d in range(4)]
    model.E = pyo.set(dim=4, initialize=station_edges)



coords = []
metrolines = get_line_data(line_station_map)

for metroline in metrolines:
    metroline = snap_grid(300, 0.1, metroline, 10)
    lines = metroline.get_lines()
    for i in range(len(lines)):
        line_coords = lines[i].get_coords()
        for coord in line_coords:
            coords.append(coord)

x = [coord[0] for coord in coords]
y = [coord[1] for coord in coords]

plt.plot(x, y, '-o')
plt.show()