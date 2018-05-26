import pygame
import random
from gridDetector import Detector
from config import *
from color import *
import sys, os

detector = Detector(150, 60, 30)
WIDTH = 350
HEIGHT = 150
FPS = 12

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
        self.image = pygame.Surface((30,30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = 30 * random.randint(0, 1)
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.touchleft = 0
        self.touchright = 0
        

    def makedecision(self):
        pass
    
    def update(self):
        self.speedx = 0
        self.touchleft = 0
        self.touchright = 0
        key = pygame.key.get_pressed()

        if self.rect.right > 40:
            self.rect.right = 60
            self.touchright = 1

        if self.rect.left < 30:
            self.rect.left = 0
            self.touchleft = 1

        if key[pygame.K_LEFT] and self.touchleft == 0:
            self.speedx = -30

        if key[pygame.K_RIGHT] and self.touchright == 0:
            self.speedx = 30

        self.rect.x += self.speedx


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 30 * random.randrange(0, 1)
        self.rect.y = 0
        self.speedy = 30

    def update(self):
        self.rect.y +=  30
        if self.rect.top > HEIGHT + 10:
            self.rect.x = 30 * random.randrange(0, 2)
            self.rect.y = 0
            self.speedy = 30


class Game(object):

    def __init__(self, neural_networks):

        pygame.init()
        pygame.mixer.init()
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

        self.all_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.neural_networks = neural_networks

        self.num_organisms = len(self.neural_networks)

        for i, neural_network in enumerate(self.neural_networks):
            play = Player(i, neural_network)
            self.all_sprites.add(play)
            self.player.add(play)


        for i in range(1):
            e = Enemy()
            self.all_sprites.add(e)
            self.enemy.add(e)

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

        self.label = self.myfont.render("Species" , 1, (255,255,0))
        self.label2 = self.myfont.render("Organism" , 1, (255,255,0))
        self.label3 = self.myfont.render("Generation" , 1, (255,255,0))
        self.label4 = self.myfont.render("Fitness" , 1, (255,255,0))
        self.label5 = self.myfont.render(str(self.fitness) , 1, (255,255,0))
        # keep loop running at the right speed
        self.clock.tick(FPS)
        # Process input (events)
        # Update
        self.all_sprites.update()

        hits = pygame.sprite.groupcollide(self.player, self.enemy, True, False)
        self.fitness += 1
        if hits:
            print('yeet')
            return

    def on_render(self):
        # Draw / render
        self.screen.fill(BLACK)
        self.screen.blit(self.label, (80, 20))
        self.screen.blit(self.label2, (80, 40))
        self.screen.blit(self.label3, (80, 60))
        self.screen.blit(self.label4, (80, 80))
        self.screen.blit(self.label5, (170, 80))
        self.all_sprites.draw(self.screen)
        # desc(screen, str(Score), 18, WIDTH / 2, 10)
        pygame.display.flip()

        for x in range(0, 2):
            for y in range(0, 5):
                if(self.screen.get_at((x*30 , y*30)) == WHITE):
                    detector.matrix[y][x] = 1

                if(self.screen.get_at((x*30 , y*30)) == RED):
                    detector.matrix[y][x] = -1


if __name__ == "__main__":
    game = Game()
    game.play()

