from color import *

class Detector:
    def __init__(self,HEIGHT, WIDTH, CELL_SIZE):
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.CELL_SIZE_X = int(WIDTH / CELL_SIZE)
        self.CELL_SIZE_Y = int(HEIGHT / CELL_SIZE)
        self.makeZero()

    def makeZero(self):
        self.matrix = [[0] * self.CELL_SIZE_X for i1 in range(self.CELL_SIZE_Y) ]
