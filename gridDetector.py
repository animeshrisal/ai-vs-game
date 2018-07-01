from color import *

WIDTH = 700
HEIGHT = 420

class Detector:
    def __init__(self,HEIGHT, WIDTH, CELL_SIZE):
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.CELL_SIZE_X = int(WIDTH / CELL_SIZE)
        self.CELL_SIZE_Y = int(HEIGHT / CELL_SIZE)
        self.makeZero()

    def makeZero(self):
        self.matrix = [[0] * self.CELL_SIZE_X for i1 in range(self.CELL_SIZE_Y) ]

    def fillMatrix(self, game):
        for enemy in game.enemy:
            x = int(enemy.rect.top / 60)
            y = int(enemy.rect.left / 60)

        if((x >= 0 and y >= 0) and (x < HEIGHT / 60)):
            game.detector.matrix[x][y] = -1
        