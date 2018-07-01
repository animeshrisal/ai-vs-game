import pygame
import random
from gridDetector import Detector
from config import *
from color import *
import sys, os
game_folder = os.path.dirname(os.path.abspath(__file__))

WIDTH = 700
HEIGHT = 420
FPS = 12000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, neural_network, id):
        pygame.sprite.Sprite.__init__(self)

        self.id = id
        self.neural_network = neural_network
        self.image = pygame.Surface((60,60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = 60 * random.randint(0, 4)
        self.rect.bottom = HEIGHT - 60
        self.speedx = 0
        self.touchleft = 0
        self.touchright = 0
        self.image = pygame.image.load(os.path.join(game_folder, "assets/ship.png"))

    def make_decision(self, detector_matrix):
        X = []
        X.append(detector_matrix[0][0])
        X.append(detector_matrix[0][1])
        X.append(detector_matrix[0][2])
        X.append(detector_matrix[0][3])
        X.append(detector_matrix[0][4])

        X.append(detector_matrix[1][0])
        X.append(detector_matrix[1][1])
        X.append(detector_matrix[1][2])
        X.append(detector_matrix[1][3])
        X.append(detector_matrix[1][4])

        X.append(detector_matrix[2][0])
        X.append(detector_matrix[2][1])
        X.append(detector_matrix[2][2])
        X.append(detector_matrix[2][3])
        X.append(detector_matrix[2][4])

        X.append(detector_matrix[3][0])
        X.append(detector_matrix[3][1])
        X.append(detector_matrix[3][2])
        X.append(detector_matrix[3][3])
        X.append(detector_matrix[3][4])


        X.append(detector_matrix[4][0])
        X.append(detector_matrix[4][1])
        X.append(detector_matrix[4][2])
        X.append(detector_matrix[4][3])
        X.append(detector_matrix[4][4])

        X.append(detector_matrix[5][0])
        X.append(detector_matrix[5][1])
        X.append(detector_matrix[5][2])
        X.append(detector_matrix[5][3])
        X.append(detector_matrix[5][4])

        X.append(detector_matrix[6][0])
        X.append(detector_matrix[6][1])
        X.append(detector_matrix[6][2])
        X.append(detector_matrix[6][3])
        X.append(detector_matrix[6][4])


        decision = self.neural_network.calculateOutput(X) 
        self.neural_network.fitness += 1
        self.speedx = 0
        self.touchleft = 0
        self.touchright = 0
        
        if self.rect.right > 260:
            self.rect.left = 240
            self.touchright = 1

        if self.rect.left < 60:
            self.rect.left = 0
            self.touchleft = 1

        if decision[0] and self.touchleft == 0:
            self.speedx = -60

        if decision[1] and self.touchright == 0:
            self.speedx = 60

        self.rect.x += self.speedx
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, id):
        self.id = id
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60,60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 60 * random.randint(0, 4)
        self.rect.y = -60 * 4 * self.id
        self.speedy = 60
        self.image = pygame.image.load(os.path.join(game_folder, "assets/asteroid.png"))
        self.movement = 0
        

    def update(self):
        self.rect.y +=  60

        if self.rect.top > HEIGHT + 200:
            self.rect.x = 60 * random.randint(0, 4)
            self.rect.y = -60 * 10
            self.speedy = 60
                    

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game(object):

    def __init__(self, neural_networks, generation_number, species_number):

        pygame.init()
        pygame.mixer.init()
        self.detector = Detector(700, 300, 60)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.fitness = 0

        def desc(surf, text, x, y):
            font = pygame.font.Font('arial', size)
            text_surface = font.render(text, True, white)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x,y)
            surf.blit(text_surface, text_rect)

        self.neural_networks = neural_networks
        self.generation_number = generation_number
        self.species_number = species_number
        self.num_organisms = len(self.neural_networks)
        
        self.players = [Player(neural_network, i) for i, neural_network in enumerate(self.neural_networks)]
        self.random_position = [0, 1, 2, 3, 4]
        self.enemy = []
        self.backgroundx1 = 0
        self.backgroundy1 = 0
        self.backgroundx2 = 0
        self.backgroundy2 = -680

        for x in range(4):
            self.enemy.append(Enemy(x))

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            if self.on_loop():
                return
            else:
                self.on_render()

    def on_loop(self):         
        keys=pygame.key.get_pressed()

        for player in self.players:
            player.make_decision(self.detector.matrix)
            player.update()

        for enemy in self.enemy:
            enemy.update()

        for i, player in enumerate(self.players):
            for j, enemy in enumerate(self.enemy):
                if player.rect.colliderect(enemy):
                    self.num_organisms = len(self.players)
                    del(self.players[i])
                    break

        if(len(self.players) == 0) or keys[pygame.K_LEFT]:
            return True
        
        self.fitness += 1
        self.backgroundy1 += 16
        self.backgroundy2 += 16

        if self.backgroundy1 > 680:
            self.backgroundy1 = -684

        if self.backgroundy2 > 680:
            self.backgroundy2 = -684


        
        self.label = self.myfont.render("Species: " + str(self.species_number), 1, (255,255,0))
        self.label2 = self.myfont.render("Organisms: " + str(self.num_organisms), 1, (255,255,0))
        self.label3 = self.myfont.render("Generation: " + str(self.generation_number), 1, (255,255,0))
        self.label4 = self.myfont.render("Fitness" , 1, (255,255,0))
        self.label5 = self.myfont.render(str(self.fitness) , 1, (255,255,0))


    def on_render(self):
        # Draw / render
        self.detector.makeZero()
        self.screen.fill(BLACK)
        self.screen.blit(pygame.image.load(os.path.join(game_folder , "assets/background.png")), (self.backgroundx1, self.backgroundy1))
        self.screen.blit(pygame.image.load(os.path.join(game_folder , "assets/background.png")), (self.backgroundx2, self.backgroundy2))
        self.screen.blit(self.label, (400, 20))
        self.screen.blit(self.label2, (400, 40))
        self.screen.blit(self.label3, (400, 60))
        self.screen.blit(self.label4, (400, 80))
        self.screen.blit(self.label5, (500, 80))
        
        for player in self.players:
            player.draw(self.screen)

        for enemy in self.enemy:
            enemy.draw(self.screen)

        '''
        for x in range(0, 4):
            for y in range(0, 6):
                if(self.screen.get_at((x*30 , y*30)) == WHITE):
                    self.detector.matrix[y][x] = 0

                if(self.screen.get_at((x*30 , y*30)) == RED):
                    self.detector.matrix[y][x] = -1

        
        '''
        
        for enemy in self.enemy:
            x = int(enemy.rect.top / 60)
            y = int(enemy.rect.left / 60)

            if((x >= 0 and y >= 0) and (x < HEIGHT / 60)):
                  self.detector.matrix[x][y] = -1
        

        print(self.detector.matrix)
        self.detector.fillMatrix(self)
        
        pygame.display.update()
        self.clock.tick(FPS)     

if __name__ == "__main__":
    game = Game()


