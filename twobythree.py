import pygame
import random
from gridDetector import Detector
from config import *
from color import *
from NEAT import NEAT

detector = Detector(150, 60, 30)
neats = NEAT()
WIDTH = 350
HEIGHT = 150
FPS = 12

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 15)
fitness = 0

def desc(surf, text, x, y):
    font = pygame.font.Font('arial', size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.touchleft = 0
        self.touchright = 0
    
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


all_sprites = pygame.sprite.Group()
enemy = pygame.sprite.Group()
player=Player()
all_sprites.add(player)

for i in range(1):
    e = Enemy()
    all_sprites.add(e)
    enemy.add(e)

running = True
while running:
    
    label = myfont.render("Species" , 1, (255,255,0))
    label2 = myfont.render("Organism" , 1, (255,255,0))
    label3 = myfont.render("Generation" , 1, (255,255,0))
    label4 = myfont.render("Fitness" , 1, (255,255,0))
    label5 = myfont.render(str(fitness) , 1, (255,255,0))
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, enemy, False)
    fitness += 1
    if hits:
        running = False
    # Draw / render
    screen.fill(BLACK)
    screen.blit(label, (80, 20))
    screen.blit(label2, (80, 40))
    screen.blit(label3, (80, 60))
    screen.blit(label4, (80, 80))
    screen.blit(label5, (170, 80))
    all_sprites.draw(screen)
    # desc(screen, str(Score), 18, WIDTH / 2, 10)
    detector.makeZero()
    pygame.display.flip()

    for x in range(0, 2):
        for y in range(0, 5):
            if(screen.get_at((x*30 , y*30)) == WHITE):
                detector.matrix[y][x] = 1

            if(screen.get_at((x*30 , y*30)) == RED):
                detector.matrix[y][x] = -1

    print(detector.matrix)

pygame.quit()