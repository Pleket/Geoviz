class MetroLine:
    def __init__(self, color):
        self.color = color
        self.lines = []
    
    def add_station(self, line):
        self.lines.append(line)
    
    def set_lines(self, lines):
        self.lines = lines
    
    def get_lines(self):
        return self.lines
    
    def get_color(self):
        return self.color

class Line:
    def __init__(self, color, station1, station2):
        self.color = color
        self.station1 = station1
        self.station2 = station2
        self.coords = []
    
    def set_stations(self, station1, station2):
        self.station1 = station1
        self.station2 = station2
    
    def set_coords(self, coords):
        self.coords = coords
    
    def add_coord(self, coord):
        self.coords.append(coord)
    
    def get_coords(self):
        return self.coords
    
    def get_stations(self):
        return (self.station1, self.station2)