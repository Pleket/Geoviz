class Station:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.lines = []
    
    def add_line(self, line):
        self.lines.append(line)
    
    def set_lines(self, lines):
        self.lines = lines
    
    def get_lines(self):
        return self.lines
    
    def get_name(self):
        return self.name
    
    def get_coordinates(self):
        return (self.x, self.y)