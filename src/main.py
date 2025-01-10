# 
# Intro:

# This game was made by Leo Sebastian Negara for Advanced python programming course in Mooc.
# The whole game is made inside a single class, which has its own methods to
# make the game functional (game logics, movement, loading etc.)


# The game:
# The game has 2 robots, which are trying to escape a blue rectangle while collecting
# coins. The goal is to collect as many coins as possible, while not getting touched by
# The rectangle. If the rectangle touches a player, all collected coins will be 
# lost. After the rectangle gets 1 player, its movement speed will increase, because
# it now has more energy to chase the other player.


# Movement:
# The monster first targets the player 1, which moves with the arrow keys, while the
# second player moves using the WASD keys

# Enjoy the game, ( best experience with 2 real players playing it )


import pygame   
import random


class Balibam:

    #Contructor:
    def __init__(self):   
        pygame.init()
        self.load_images()
        self.initialize_positions()
        self.handle_movements()
    
    def load_images(self):
        self.images = {}
        image_names = ["coin", "door", "monster", "robot"]
        for name in image_names:
            self.images[name] = pygame.image.load(f"src/{name}.png")

        self.window = pygame.display.set_mode((640, 480))

        self.game_font = pygame.font.SysFont("Arial", 24)

    def initialize_positions(self):
        self.x, self.y = 0, 480 - self.images['robot'].get_height()
        self.r, self.t = 90, 480 - self.images['robot'].get_height()
        self.i, self.o = 200, 300 - self.images['monster'].get_height()
        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False


        self.s_right = False
        self.s_left = False
        self.s_up = False
        self.s_down = False

        self.coincounter = 0

        self.firstrobotlives = 1
        self.secondrobotlives = 1
        

    def generate_random_position(self):
        self.c = random.randint(0, self.window.get_width() - self.images['coin'].get_width())
        self.v = random.randint(0, self.window.get_height() - self.images['coin'].get_height())
        return self.c, self.v

    def handle_movements(self):
        clock = pygame.time.Clock()
        self.coin_position = self.generate_random_position()  # Generates the initial coin position
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                if event.type == pygame.KEYUP:
                    self.handle_keyup(event)
                if event.type == pygame.QUIT:
                    exit()

            # Collision detection for the first robot and the coin
            if self.detect_collision((self.x, self.y), self.coin_position, self.images['robot'], self.images['coin']):
                self.coin_position = self.generate_random_position()  # Spawn coin in a new random position
                self.coincounter += 1

            # Collision detection for the second robot and the coin
            if self.detect_collision((self.r, self.t), self.coin_position, self.images['robot'], self.images['coin']):
                self.coin_position = self.generate_random_position()  # Spawn coin in a new random position
                self.coincounter += 1

            if self.detect_collision((self.x, self.y), (self.i, self.o), self.images['robot'], self.images['monster']):
                self.coincounter = 0
                self.firstrobotlives -=1
            
            if self.detect_collision((self.r, self.t), (self.i, self.o), self.images['robot'], self.images['monster']):
                self.coincounter = 0
                self.secondrobotlives -=1



            if self.firstrobotlives > 0:
                self.move_robot()
            if self.secondrobotlives >0:
                self.move_second_robot()
            
         

            self.move_monster()

            self.window.fill((0, 0, 0))
            self.window.blit(self.images['robot'], (self.x, self.y))
            self.window.blit(self.images['robot'], (self.r, self.t))
            self.window.blit(self.images['coin'], self.coin_position)
            self.window.blit(self.images['door'], (self.i, self.o))

            
            self.points = self.game_font.render(f"Coins collected: {self.coincounter}", True, (255, 0, 0))
            self.window.blit(self.points, (460, 10))
            pygame.display.flip()

            clock.tick(60)

    def detect_collision(self, robot_position, coin_position, robot_image, coin_image):
        robot_rect = pygame.Rect(*robot_position, robot_image.get_width(), robot_image.get_height())
        coin_rect = pygame.Rect(*coin_position, coin_image.get_width(), coin_image.get_height())
        return robot_rect.colliderect(coin_rect)

    def handle_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.to_left = True
        if event.key == pygame.K_RIGHT:
            self.to_right = True
        if event.key == pygame.K_UP:
            self.to_up = True
        if event.key == pygame.K_DOWN:
            self.to_down = True
            ####
            # Other keydown events for robot movement
        # ...
                
        if event.key == pygame.K_a:  # Handling second robot's LEFT movement
            self.s_left = True
        if event.key == pygame.K_d:  # Handling second robot's RIGHT movement
            self.s_right = True
        if event.key == pygame.K_w:  # Handling second robot's UP movement
            self.s_up = True
        if event.key == pygame.K_s:  # Handling second robot's DOWN movement
            self.s_down = True        

        

    def handle_keyup(self, event):
        if event.key == pygame.K_LEFT:
            self.to_left = False
        if event.key == pygame.K_RIGHT:
            self.to_right = False
        if event.key == pygame.K_UP:
            self.to_up = False
        if event.key == pygame.K_DOWN:
            self.to_down = False

        # Other keyup events for robot movement
        # ...
        if event.key == pygame.K_a:  # Handling second robot's LEFT key release
            self.s_left = False
        if event.key == pygame.K_d:  # Handling second robot's RIGHT key release
            self.s_right = False
        if event.key == pygame.K_w:  # Handling second robot's UP key release
            self.s_up = False
        if event.key == pygame.K_s:  # Handling second robot's DOWN key release
            self.s_down = False


    def move_robot(self):
        if self.to_right and self.x + self.images['robot'].get_width() < self.window.get_width():
            self.x += 6
        if self.to_left and self.x > 0:
            self.x -= 6
        if self.to_up and self.y >0:
            self.y -= 6
        if self.to_down and self.y + self.images['robot'].get_height() < self.window.get_height():
            self.y += 6

        # Other movement conditions for the first robot
        # ...

    def move_second_robot(self):
        if self.s_right and self.r + self.images['robot'].get_width() < self.window.get_width():
            self.r += 6
        if self.s_left and self.r > 0:
            self.r -= 6
        if self.s_up and self.t >0:
            self.t -= 6
        if self.s_down and self.t + self.images['robot'].get_height() < self.window.get_height():
            self.t += 6
        # Other movement conditions for the second robot
        # ...
    
    def move_monster(self):

        if self.firstrobotlives > 0:
            if self.x > self.i:
                self.i += 1
            if self.x < self.i:
                self.i -= 1
            if self.y > self.o:
                self.o += 1
            if self.y < self.o:
                self.o -= 1
        else:     
            if self.r > self.i:
                self.i += 1.5
            if self.r < self.i:
                self.i -= 1.5
            if self.t > self.o:
                self.o += 1.5
            if self.t < self.o:
                self.o -= 1.5
        

# Instantiates the Balibam class to run the game
game = Balibam()