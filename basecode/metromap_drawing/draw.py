import drawsvg as draw
import numpy as np
import math as Math

def draw_circle(x, y, lines, d, line_thickness=2, color='none'):
    """
    Draw a circle 'station' on the drawing object.

    Parameters:
    - x (float): The x-coordinate of the center of the circle.
    - y (float): The y-coordinate of the center of the circle.
    - lines (int): The number of lines to draw within the circle.
    - d (draw.Drawing): The drawing object to add the circle to.
    - line_thickness (int, optional): The thickness of the lines of the tracks coming in and going out. Default is 2.
    - color (str, optional): The color of the circle. Default is 'none'.

    Returns:
    - None
    """
    
    r = (lines*line_thickness + lines - 1) / 2
    d.append(draw.Circle(x, y, r, stroke='black', fill=color))

def draw_rectangle_station(x, y, lines_h, lines_v, d, line_thickness=2, color='none'):
    """
    Draw a rectangle 'station' on the drawing object with smooth corners.

    Parameters:
    - x (float): The x-coordinate of the top-left corner of the rectangle.
    - y (float): The y-coordinate of the top-left corner of the rectangle.
    - lines_h (int): The number of horizontal lines coming in/going out.
    - lines_v (int): The number of vertical lines coming in/going out.
    - d (draw.Drawing): The drawing object to add the rectangle to.
    - line_thickness (int, optional): The thickness of the lines of the tracks coming in and going out. Default is 2.
    - color (str, optional): The color of the rectangle. Default is 'none'.

    Returns:
    - None
    """

    r = line_thickness / 2
    c_h = -0.5
    c_v = -0.5

    if (lines_h == 0):
        lines_h = 1
        c_h = 0.5
    if (lines_v == 0):
        lines_v = 1
        c_v = 0.5

    r_h = lines_h*line_thickness + lines_h - c_h
    r_v = lines_v*line_thickness + lines_v - c_v

    d.append(draw.Rectangle(x, y, r_v, r_h, rx = r, ry = r, stroke='black', fill=color, transform='translate({correction_x},{correction_y})'.format(correction_x=-((r_v - 1) / 2), correction_y=-((r_h - 1) / 2))))

def draw_rectangle_station_rotate(x, y, lines_h, lines_v, d, line_thickness=2, color='none', center=(0,0)):
    """
    Draw a rotated rectangle 'station' on the drawing object with smooth corners, where the rotation is determined by its position toward some center.

    Parameters:
    - x (float): The x-coordinate of the top-left corner of the rectangle.
    - y (float): The y-coordinate of the top-left corner of the rectangle.
    - lines_h (int): The number of horizontal lines coming in/going out.
    - lines_v (int): The number of vertical lines coming in/going out.
    - d (draw.Drawing): The drawing object to add the rectangle to.
    - line_thickness (int, optional): The thickness of the lines of the tracks coming in and going out. Default is 2.
    - color (str, optional): The color of the rectangle. Default is 'none'.
    - center (tuple, optional): The coordinates of the center of the rotation. Default is (0,0)

    Returns:
    - None
    """

    if x - center[0] == 0:
        draw_rectangle_station(x, y, lines_h, lines_v, d, line_thickness, color)
        return

    r = line_thickness / 2
    c_h = -0.5
    c_v = -0.5

    if (lines_h == 0):
        lines_h = 1
        c_h = 0.5
    if (lines_v == 0):
        lines_v = 1
        c_v = 0.5

    r_h = lines_h*line_thickness + lines_h - c_h
    r_v = lines_v*line_thickness + lines_v - c_v

    angle = Math.atan2(y - center[1], x - center[0]) * 180 / np.pi

    d.append(draw.Rectangle(x, y, r_h, r_v, rx = r, ry = r, stroke='black', fill=color, transform='rotate({angle},{x},{y}) translate({correction_x},{correction_y})'.format(angle=angle, x=x, y=y, correction_x=-((r_h - 1) / 2), correction_y=-((r_v - 1) / 2))))

def draw_lines(x_source, y_source, x_target, y_target, lines, d, line_thickness=2, colors=['black'], rotate = False):
    """
    Draw a set of lines between two points on the drawing object.
    
    Parameters:
    - x_source (float): The x-coordinate of the source station.
    - y_source (float): The y-coordinate of the source station.
    - x_target (float): The x-coordinate of the target station.
    - y_target (float): The y-coordinate of the target station.
    - lines (int): The number of lines to draw between the source and target points.
    - d (draw.Drawing): The drawing object to add the lines to.
    - line_thickness (int, optional): The thickness of the lines. Default is 2.
    - colors (list, optional): The colors of the lines. Default is ['black'].
    - rotate (bool, optional): Whether to rotate the lines's endpoints when the line direction is not horizontal or vertical. Default is False.
    
    Returns:
    - None
    """

    thickness_x = line_thickness
    space_x = 1
    r = ((lines - 1) / 2) * (thickness_x + space_x)
    if (lines % 2 == 0):
        r = ((lines/2) - 1) * (thickness_x + space_x) + (thickness_x + space_x) / 2
    a = 1
    a_p = 0

    if (x_target - x_source) != 0 and rotate:
        a, a_p, thickness_x, space_x, r = calculate_rotation_xy(x_source, y_source, lines, center=(x_target, y_target), line_thickness=line_thickness)

    source_coords = [(x_source - r + i * (thickness_x + space_x), y_source - r * a_p + i * (thickness_x + space_x) * a_p) for i in range(int(lines))]
    target_coords = [(x_target - r + i * (thickness_x + space_x), y_target - r * a_p + i * (thickness_x + space_x) * a_p) for i in range(int(lines))]

    for i in range(lines):
        d.append(draw.Line(source_coords[i][0], source_coords[i][1], target_coords[i][0], target_coords[i][1], stroke=colors[i], stroke_width=line_thickness))

def draw_curves(x_source, y_source, x_target, y_target, lines, d, line_thickness=2, colors=['black'], center=(0,0)):
    """
    Draw a set of lines between two points on the drawing object, curved around a center pivot. 
    
    Parameters:
    - x_source (float): The x-coordinate of the source station.
    - y_source (float): The y-coordinate of the source station.
    - x_target (float): The x-coordinate of the target station.
    - y_target (float): The y-coordinate of the target station.
    - lines (int): The number of lines to draw between the source and target points.
    - d (draw.Drawing): The drawing object to add the lines to.
    - line_thickness (int, optional): The thickness of the lines. Default is 2.
    - colors (list, optional): The colors of the lines. Default is ['black'].
    - center (tuple, optional): The coordinates of the center of the rotation. Default is (0,0)
    
    Returns:
    - None
    """

    if (x_source - center[0])**2 + (y_source - center[1])**2 != (x_target - center[0])**2 + (y_target - center[1])**2:
        raise ValueError("The source and target points must be at the same distance from the center!")

    thickness_y_source = line_thickness
    space_y_source = line_thickness / 2
    r_source = ((lines - 1) / 2) * (thickness_y_source + space_y_source)
    if (lines % 2 == 0):
        r = ((lines/2) - 1) * (thickness_y_source + space_y_source) + (thickness_y_source + space_y_source) / 2
    a_source = 1
    a_p_source = 0

    if (x_source - center[0]) != 0:
        a_source, a_p_source, thickness_y_source, space_y_source, r_source = calculate_rotation_xy(x_source, y_source, lines, center=(x_target, y_target), line_thickness=line_thickness)

    thickness_y_target = line_thickness
    space_y_target = line_thickness / 2
    r_source = ((lines - 1) / 2) * (thickness_y_target + space_y_target)
    if (lines % 2 == 0):
        r = ((lines/2) - 1) * (thickness_y_target + space_y_target) + (thickness_y_target + space_y_target) / 2
    a_target = 1
    a_p_target = 0

    if (x_target - center[0]) != 0:
        a_target, a_p_target, thickness_y_target, space_y_target, r_target = calculate_rotation_xy(x_source, y_source, lines, center=(x_target, y_target), line_thickness=line_thickness)

    source_coords = [(x_source + r_source * a_p_source - i * (thickness_y_source + space_y_source) * a_p_source, y_source - r_source + i * (thickness_y_source + space_y_source)) for i in range(int(lines))]
    target_coords = [(x_target - r_target * a_p_target + i * (thickness_y_target + space_y_target) * a_p_target, y_target + r_target - i * (thickness_y_target + space_y_target)) for i in range(int(lines))]
    dists_center = [(np.sqrt((s[0] - center[0])**2 + (s[1] - center[1])**2)) for s in source_coords]

    for i in range(lines):
        p = draw.Path(stroke=colors[i], stroke_width=line_thickness, fill='none')
        d.append(p.M(source_coords[i][0], source_coords[i][1]).A(dists_center[i], dists_center[i], 0, 0, 1, target_coords[i][0], target_coords[i][1]))

def calculate_rotation_xy(x, y, lines, center=(0,0), line_thickness=2):
    """
    Helper function to calculate the rotation of the lines's endpoints when the line direction is not horizontal or vertical.

    Parameters:
    - x (float): The x-coordinate of the source station.
    - y (float): The y-coordinate of the source station.
    - lines (int): The number of lines to be drawn. 
    - center (tuple, optional): The coordinates of the center in which direction the lines should point. Default is (0,0).
    - line_thickness (int, optional): The thickness of the lines. Default is 2.
    """

    a = (center[1] - y) / abs(center[0] - x)
    a_p = -1/a

    thickness_x = np.sqrt(line_thickness**2 / (1 + a_p**2))
    space_x = np.sqrt(1 / (1 + a_p**2))
    r = ((lines - 1) / 2) * (thickness_x + space_x)
    if (lines % 2 == 0):
        r = ((lines/2) - 1) * (thickness_x + space_x) + (thickness_x + space_x) / 2
    # Compute the x value from the slope a
    r = np.sqrt(r ** 2 / (1 + a_p**2))

    return a, a_p, thickness_x, space_x, r

dr = draw.Drawing(300, 300, origin='center')

# draw_circle(-40, -120, 5, dr, 2)
# draw_circle(40, 85, 5, dr, 2)
# draw_lines(-40, -120, 40, 85, 5, dr, 2, ['red', 'green', 'blue', 'yellow', 'purple'])

# draw_lines(-40, -120, 40, 120, 5, dr, 2, ['red', 'green', 'blue', 'yellow', 'purple'], True)
draw_curves(-40, -120, 40, 120, 5, dr, 2, ['red', 'green', 'blue', 'yellow', 'purple'])
draw_rectangle_station_rotate(-40, -120, 5, 0, dr, 2)
draw_rectangle_station_rotate(40, 120, 5, 0, dr, 2)

dr.set_pixel_scale(5)
#d.set_render_size(400, 200)
dr.save_svg('test.svg')