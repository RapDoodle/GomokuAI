class Piece():

    def __init__(self, color):
        if color not in ['B', 'W']:
            raise Exception('Invalid color')
        self.color = color
    
    def __str__(self):
        return self.color