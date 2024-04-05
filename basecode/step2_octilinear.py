from enum import Enum
import pyomo as pyo


def snap_grid(bounding_box, square_size, metroline):
    # Create a dictionary to store the snapped coordinates
    lines = metroline.get_lines()

    # Iterate over the metroline stations
    for i in range(len(lines)):
        line = lines[i]

        coord1 = line.get_stations()[0].get_coordinates()
        coord2 = line.get_stations()[1].get_coordinates()
        
        dist_1 = ((coord1[0] - (coord1[0] % square_size)) / square_size, (coord1[1] - (coord1[1] - square_size)) / square_size)
        dist_2 = ((coord2[0] - (coord2[0] % square_size)) / square_size, (coord2[1] - (coord2[1] - square_size)) / square_size)

        corner1 = compute_corner(square_size, coord1)
        corner2 = compute_corner(square_size, coord2)

        new_coord_1 = ((dist_1[0] + corner1.value[0]) * square_size, (dist_1[1] + corner1.value[1]) * square_size)
        new_coord_2 = ((dist_2[0] + corner2.value[0]) * square_size, (dist_2[1] + corner2.value[1]) * square_size)

        line_path = find_grid_path(new_coord_1, new_coord_2, square_size)
        lines[i].set_coords(line_path)
        lines[i].station1.set_coordinates(new_coord_1)
        lines[i].station2.set_coordinates(new_coord_2)
    
    return metroline

def find_grid_path(coord1, coord2, square_size):
    current_coord = tuple(coord1[0], coord1[1])
    path = [tuple(coord1[0], coord1[1])]

    while current_coord[0] != coord2[0] and current_coord[1] != coord2[1]:
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
        
        path.append(tuple(new_x, new_y))
        current_coord = tuple(new_x, new_y)
    
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

