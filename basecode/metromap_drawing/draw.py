import drawsvg as draw
import numpy as np
import math as Math

def draw_circle(x, y, lines, d, line_thickness=2, color='none'):
    r = (lines*line_thickness + lines - 1) / 2
    d.append(draw.Circle(x, y, r, stroke='black', fill=color))

def draw_rectangle_station(x, y, lines_h, lines_v, d, line_thickness=2, color='none', center=(0,0)):
    r = line_thickness / 2

    if (lines_h == 0):
        lines_h = 1
    if (lines_v == 0):
        lines_v = 1

    r_h = lines_h*line_thickness + lines_h - 1
    r_v = lines_v*line_thickness + lines_v - 1

    angle = Math.atan2(y - center[1], x - center[0]) * 180 / np.pi

    d.append(draw.Rectangle(x, y, r_h, r_v, rx = r, ry = r, stroke='black', fill=color, transform = 'rotate({angle},{x},{y})'.format(angle=angle, x=x, y=y)))

def draw_lines(x_source, y_source, x_target, y_target, lines, d, line_thickness=2, colors=['black']):
    a = (y_target - y_source) / abs(x_target - x_source)
    # b = y_source - a*x_source
    a_p = -1/a
    # b_p = y_source - a_p*x_source

    thickness_x = np.sqrt(line_thickness**2 / (1 + a_p**2))
    space_x = np.sqrt(1 / (1 + a_p**2))
    r = ((lines - 1) / 2) * (thickness_x + space_x)
    if (lines % 2 == 0):
        r = ((lines/2) - 1) * (thickness_x + space_x) + (thickness_x + space_x) / 2
    # Compute the x value from the slope a
    r = np.sqrt(r ** 2 / (1 + a_p**2))

    source_coords = [(x_source - r + i * (thickness_x + space_x), y_source - r * a_p + i * (thickness_x + space_x) * a_p) for i in range(int(lines))]
    target_coords = [(x_target - r + i * (thickness_x + space_x), y_target - r * a_p + i * (thickness_x + space_x) * a_p) for i in range(int(lines))]

    for i in range(lines):
        d.append(draw.Line(source_coords[i][0], source_coords[i][1], target_coords[i][0], target_coords[i][1], stroke=colors[i], stroke_width=line_thickness))
    
dr = draw.Drawing(300, 300, origin='center')

# draw_circle(-40, -120, 5, dr, 2)
# draw_circle(40, 85, 5, dr, 2)
# draw_lines(-40, -120, 40, 85, 5, dr, 2, ['red', 'green', 'blue', 'yellow', 'purple'])

draw_rectangle_station(-40, -120, 0, 5, dr, 2)
draw_rectangle_station(40, 85, 0, 5, dr, 2)
draw_lines(-40, -120, 40, 85, 5, dr, 2, ['red', 'green', 'blue', 'yellow', 'purple'])

dr.set_pixel_scale(5)
#d.set_render_size(400, 200)
dr.save_svg('test.svg')