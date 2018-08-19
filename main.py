import pygame
import random
from gridDetector import Detector
from config import *
from color import *
import sys, os
import pickle
game_folder = os.path.dirname(os.path.abspath(__file__))

WIDTH = 700
HEIGHT = 420
FPS = 12

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, id, neural_network = None):
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
        self.lives = 5

        self.images = []
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/ship/ship11.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/ship/ship12.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/ship/ship13.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/ship/ship14.png")))

        self.image_index = 0
        self.image = self.images[self.image_index]

    def player_movement(self):
        keys=pygame.key.get_pressed()

        self.speedx = 0
        self.touchleft = 0
        self.touchright = 0
        
        if self.rect.right > 260:
            self.rect.left = 240
            self.touchright = 1

        if self.rect.left < 60:
            self.rect.left = 0
            self.touchleft = 1

        if keys[pygame.K_LEFT] and self.touchleft == 0:
            self.speedx = -60

        if keys[pygame.K_RIGHT] and self.touchright == 0:
            self.speedx = 60

        self.rect.x += self.speedx

    def make_decision(self, detector_matrix):
        X = []

        for x in range(7):
            for y in range(5):
                X.append(detector_matrix[x][y])


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
        self.image_index += 1

        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[self.image_index]

        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60,60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 60

        self.images = []
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid1.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid2.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid3.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid4.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid5.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid6.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid7.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid8.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid9.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid10.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid11.png")))
        self.images.append(pygame.image.load(os.path.join(game_folder, "assets/asteroid/asteroid12.png")))
        self.image_index = random.randint(0,11)
        self.image = self.images[self.image_index]

        self.movement = 0
        
    def vs_update(self, id , enemy_list):
        self.rect.y +=  60
        self.same_position = True

        if self.rect.top > HEIGHT + 20:
            self.rect.x = 60 * random.randint(0, 4)
            self.rect.y = -60 * 10 * random.randint(0, 4)
            self.speedy = 60

    def click_update(self, id ,  enemy_list):
        self.rect.y +=  60
        self.same_position = True

        if self.rect.top > HEIGHT + 20:
                '''
                self.rect.x = 30 * random.randint(0, 4)
                self.rect.y = -30 * random.randint(0, 8)
                self.speedy = 30
                '''
                del(enemy_list[id])
                                
    def draw(self, screen):
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[self.image_index]
        screen.blit(self.image, self.rect)


class Game(object):

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.detector = Detector(420, 300, 60)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.fitness = 0
        self.total_collision_object_count = 0
        self.number_of_ai_collisions = 0

        self.neat = pickle.load(open("aiagent.p", "rb"))
        self.enemy = []
        self.backgroundx1 = 0
        self.backgroundy1 = 0
        self.backgroundx2 = 0
        self.backgroundy2 = -680
        self.human = Player(0)
        self.player = Player(1, self.neat)
        self.increase_enemy_counter = 0

        for x in range(0):
            self.enemy.append(Enemy(x))

        def desc(surf, text, x, y):
            font = pygame.font.Font('arial', size)
            text_surface = font.render(text, True, white)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x,y)
            surf.blit(text_surface, text_rect)

    def menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            keys=pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                return 1

            if keys[pygame.K_RIGHT]:
                return 2

            self.screen.fill(BLACK)
            self.label = self.myfont.render("Species", 1, (255,255,0))
            self.screen.blit(self.label, (20, 20))

            pygame.display.update()
            self.clock.tick(FPS) 


    def play(self, choice):
        if choice == 1:
            while True:
                self.vs_on_loop()
                self.vs_on_render()
        
        if choice == 2:
            while True:
                self.click_on_loop()
                self.click_on_render()

    def click_on_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if self.mouse[0] < 300 and self.mouse[1] < 180:
            x = self.mouse[0] - self.mouse[0] % 60
            y = self.mouse[1] - self.mouse[1] % 60

            if self.click[0] == 1 and self.mouse_limit == 0:
                if len(self.enemy) < 2:
                    self.mouse_limit = 1
                    self.enemy.append(Enemy(x , y))
            
            else:
                self.mouse_limit = 0
            
        self.player.make_decision(self.detector.matrix)
        self.player.update()

        for i, enemy in enumerate(self.enemy):
            enemy.click_update(i, self.enemy)

        for j, enemy in enumerate(self.enemy):
            if self.player.rect.colliderect(enemy):
                del(self.player)
                return True

        
        self.fitness += 1
        self.backgroundy1 += 16
        self.backgroundy2 += 16

        if self.backgroundy1 > 680:
            self.backgroundy1 = -684

        if self.backgroundy2 > 680:
            self.backgroundy2 = -684


    def click_on_render(self):
                # Draw / render
        self.detector.makeZero()
        self.screen.fill(BLACK)
        self.screen.blit(pygame.image.load(os.path.join(game_folder , "assets/background.png")), (self.backgroundx1, self.backgroundy1))
        self.screen.blit(pygame.image.load(os.path.join(game_folder , "assets/background.png")), (self.backgroundx2, self.backgroundy2))

        self.player.draw(self.screen)

        for enemy in self.enemy:
            enemy.draw(self.screen)

        for enemy in self.enemy:
            x = int(enemy.rect.top / 60)
            y = int(enemy.rect.left / 60)

            if((x >= 0 and y >= 0) and (x < HEIGHT / 60)):
                  self.detector.matrix[x][y] = -1
        
        print(self.detector.matrix)
        pygame.display.update()
        self.clock.tick(FPS)   

    def vs_on_loop(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        for j, enemy in enumerate(self.enemy):
            if self.player.rect.colliderect(enemy):
                self.number_of_ai_collisions += 1
                self.player.lives -= 1
                print(self.player.lives)
                print("AI Player has collided")

            if self.human.rect.colliderect(enemy):
                self.human.lives -= 1
                print(self.human.lives)
                print("Human Player has collided")

        for enemy in self.enemy:
            enemy.vs_update(self, self.enemy)

        
        value = self.increase_enemy_counter % 200
        if(value == 0):
            enemy_value = self.increase_enemy_counter / 200
            self.enemy.append(Enemy(enemy_value, 0))

        self.player.make_decision(self.detector.matrix)
        self.human.player_movement()
        
        self.fitness += 1
        self.increase_enemy_counter += 1
        self.backgroundy1 += 16
        self.backgroundy2 += 16

        if self.backgroundy1 > 680:
            self.backgroundy1 = -684

        if self.backgroundy2 > 680:
            self.backgroundy2 = -684

    def vs_on_render(self):
        # Draw / render
        self.detector.makeZero()
        self.screen.fill(BLACK)
        self.screen.blit(pygame.image.load(os.path.join(game_folder , "assets/background.png")), (self.backgroundx1, self.backgroundy1))
        self.screen.blit(pygame.image.load(os.path.join(game_folder , "assets/background.png")), (self.backgroundx2, self.backgroundy2))

        for enemy in self.enemy:
            enemy.draw(self.screen)

        self.player.draw(self.screen)
        self.human.draw(self.screen)


        self.detector.fillMatrix(self)
        print(self.detector.matrix)

        pygame.display.update()
        self.clock.tick(FPS) 

if __name__ == "__main__":
    game = Game()
    choice = game.menu()
    print(choice)
    game.play(choice)


