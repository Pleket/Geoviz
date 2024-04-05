class MetroLine:
    def __init__(self, color):
        self.color = color
        self.lines = []
        self.turns= []
        self.i = 0
    
    def add_line(self, line):
        line.set_index(self.i)
        self.lines.append(line)
        self.i += 1
    
    def set_lines(self, lines):
        self.lines = lines
        self.i = len(lines)
    
    def get_lines(self):
        return self.lines
    
    def get_color(self):
        return self.color   

    def get_turns(self):
        turns = []
        for i in self.lines:
            turns.append(i.get_turns())
        return turns

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
    
    def get_color(self):
        return self.color  
    
    def get_turns(self):
        turns = []
        for i in range(len(self.coords)-2):
            if (self.coords[i+1][1]-self.coords[i][1])/((self.coords[i+1][0]-self.coords[i][0])) != (self.coords[i+2][1]-self.coords[i+1][1])/((self.coords[i+2][0]-self.coords[i+1][0])):
                turns.append(i)
        return turns
    
    def set_index(self, i):
        self.index = i
    
    def get_id(self):
        return self.color + str(self.index)