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
        if self.id == 0:
            self.image = pygame.image.load(os.path.join(game_folder, "assets/player.png"))
        else:
            self.image = pygame.image.load(os.path.join(game_folder, "assets/ship.png"))

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
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, id):
        self.id = id
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60,60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 60 * random.randint(0, 4)
        self.rect.y = -60 * 10 * self.id
        self.speedy = 60
        self.image = pygame.image.load(os.path.join(game_folder, "assets/asteroid.png"))
        self.movement = 0
        
    def update(self, game):
        self.rect.y +=  60

        if self.rect.top > HEIGHT + 200:
            game.total_collision_object_count += 1
            self.rect.x = 60 * random.randint(0, 4)
            self.rect.y = -60 * 10 * self.id
            self.speedy = 60
                    
    def draw(self, screen):
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
        self.player = Player(0)
        self.aiagent = Player(1, self.neat)
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
            enemy.update(i, self.enemy)

        for j, enemy in enumerate(self.enemy):
            if player.rect.colliderect(enemy):
                del(self.player)
                break

        if(len(self.players) == 0):
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
        pygame.display.update()
        self.clock.tick(FPS)   

    def vs_on_loop(self):    
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        for j, enemy in enumerate(self.enemy):
            if self.aiagent.rect.colliderect(enemy):
                self.number_of_ai_collisions += 1
                print("AI has collided")

            if self.player.rect.colliderect(enemy):
                print("Player has collided")

        for enemy in self.enemy:
            enemy.update(self)

        print("Total Number of Collision Objects: " + str(self.total_collision_object_count))

        if self.number_of_ai_collisions == 0:
            print("Accuracy: 100%")
        else:
            percentage = ((self.total_collision_object_count - self.number_of_ai_collisions) / self.total_collision_object_count) * 100
            print("Accuracy:" + str(percentage))
        
        value = self.increase_enemy_counter % 200
        if(value == 0):
            enemy_value = self.increase_enemy_counter / 200
            self.enemy.append(Enemy(enemy_value))

        self.aiagent.make_decision(self.detector.matrix)
        self.player.player_movement()
        
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

        self.aiagent.draw(self.screen)
        self.player.draw(self.screen)


        self.detector.fillMatrix(self)
        print(self.detector.matrix)

        pygame.display.update()
        self.clock.tick(FPS) 

if __name__ == "__main__":
    game = Game()
    choice = game.menu()
    print(choice)
    game.play(choice)


