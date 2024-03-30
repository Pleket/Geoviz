import drawsvg as draw
import numpy as np
import math as Math

def draw_circle(x, y, lines, d, line_thickness=2, color='none'):
    r = (lines*line_thickness + lines - 1) / 2
    d.append(draw.Circle(x, y, r, stroke='black', fill=color))

def draw_rectangle_station(x, y, lines_h, lines_v, d, line_thickness=2, color='none'):
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

    d.append(draw.Rectangle(x, y, r_v, r_h, rx = r, ry = r, stroke='black', fill=color, transform='translate({correction},0)'.format(correction=-((r_v - 1) / 2))))

def draw_rectangle_station_rotate(x, y, lines_h, lines_v, d, line_thickness=2, color='none', center=(0,0)):
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

    d.append(draw.Rectangle(x, y, r_h, r_v, rx = r, ry = r, stroke='black', fill=color, transform='rotate({angle},{x},{y}) translate(0,{correction})'.format(angle=angle, x=x, y=y, correction=-((r_v - 1) / 2))))


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

def draw_curve(x_source, y_source, x_target, y_target, lines, d, line_thickness=2, colors=['black'], center=(0,0)):
    if (x_source - center[0])**2 + (y_source - center[1])**2 != (x_target - center[0])**2 + (y_target - center[1])**2:
        raise ValueError("The source and target points must be at the same distance from the center!")

    a_source = (center[1] - y_source) / abs(center[0] - x_source)
    a_p_source = -1/a_source

    thickness_x_source = np.sqrt(line_thickness**2 / (1 + a_source**2))
    space_x_source = np.sqrt(1 / (1 + a_source**2))
    r_source = ((lines - 1) / 2) * (thickness_x_source + space_x_source)
    if (lines % 2 == 0):
        r_source = ((lines/2) - 1) * (thickness_x_source + space_x_source) + (thickness_x_source + space_x_source) / 2

    a_target = (center[1] - y_source) / abs(center[0] - x_source)
    a_p_target = -1/a_source

    thickness_x_target = np.sqrt(line_thickness**2 / (1 + a_target**2))
    space_x_target = np.sqrt(1 / (1 + a_target**2))
    r_target = ((lines - 1) / 2) * (thickness_x_target + space_x_target)
    if (lines % 2 == 0):
        r_target = ((lines/2) - 1) * (thickness_x_target + space_x_target) + (thickness_x_target + space_x_target) / 2

    source_coords = [(x_source - r_source + i * (thickness_x_source + space_x_source), y_source - r_source * a_p_source + i * (thickness_x_source + space_x_source) * a_p_source) for i in range(int(lines))]
    target_coords = [(x_target - r_target + i * (thickness_x_target + space_x_target), y_target - r_target * a_p_target + i * (thickness_x_target + space_x_target) * a_p_source) for i in range(int(lines))]
    dists_center = [(np.sqrt((s[0] - center[0])**2 + (s[1] - center[1])**2)) for s in source_coords]

    for i in range(len(lines)):
        p = draw.Path(stroke=colors[i], stroke_width=line_thickness)
        d.append(p.M(source_coords[i][0], source_coords[i][1]).A(dists_center[i], dists_center[i], 0, 0, 1, target_coords[i][0], target_coords[i][1]))
    
dr = draw.Drawing(300, 300, origin='center')

# draw_circle(-40, -120, 5, dr, 2)
# draw_circle(40, 85, 5, dr, 2)
# draw_lines(-40, -120, 40, 85, 5, dr, 2, ['red', 'green', 'blue', 'yellow', 'purple'])

draw_lines(-40, -120, 40, 120, 5, dr, 2, ['red', 'green', 'blue', 'yellow', 'purple'])
draw_rectangle_station(-40, -120, 0, 5, dr, 2)
draw_rectangle_station(40, 120, 0, 5, dr, 2)

dr.set_pixel_scale(5)
#d.set_render_size(400, 200)
dr.save_svg('test.svg')