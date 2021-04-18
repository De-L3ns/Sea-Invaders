import pygame
import random

# Initialize game window here
pygame.init()

# Variables for the game window
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Sea Invaders')
clock = pygame.time.Clock()  # Adds the clock for spawn timers

# Sprites, background and music
background = pygame.image.load('Background.jpg')
whale_sprite = pygame.image.load('Whale.png')
speedboat_sprite = pygame.image.load('Speedboat.png')
beam_sprite = pygame.image.load('Beam.png')


# Classes
class Player():

    def __init__(self, x, y, width, height):
        # Variables for the Whale go here
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mov_speed = 5
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, window):
        # This function draws the whale using the sprite and the defined location in the class parameters
        window.blit(whale_sprite, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


class Enemy():

    def __init__(self, x, y, width, height, mov_speed, sprite):
        # Variables for the various enemies
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mov_speed = mov_speed
        self.sprite = sprite
        self.hitbox = (self.x + 22, self.y + 15, 19, 45)  # Dimensions of the hitbox to make it close to the model
        self.alive = True

    def draw(self, window):
        # This function draws the enemy with the pre-defined sprite and location
        if self.alive:
            window.blit(self.sprite, (self.x, self.y))
            self.hitbox = (self.x + 22, self.y + 15, 19, 45)  # Dimensions of the hitbox to make it close to the model
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def move(self):
        # This function lets the enemy go forward until the end of the screen
        max_distance = 800 - self.height
        if self.y < max_distance:
            self.y += self.mov_speed
        if self.y >= max_distance:
            self.alive = False

    def hit(self):
        self.alive = False



class Projectile():
    def __init__(self, x, y, width, height, speed, sprite):
        # Variables for the player attacks (ranged)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.sprite = sprite

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))


# Methods
def redrawGameWindow():
    window.blit(background, (0, 0))  # Loads in the background
    whale.draw(window)  # Draws the Whale in the game

    for speedboat in speedboats:
        speedboat.draw(window)
        speedboat.move()

    for fired_beam in beams:
        fired_beam.draw(window)
    pygame.display.update()  # This updates the above changes to the game window


def startMessage():
    font = pygame.font.SysFont('comicsans', 32)
    text = font.render('Try to destroy as many boats as possible to save the ocean!', True, (255, 0, 0))
    window.blit(text, text.get_rect(center=window.get_rect().center))


# Game logic here
game = True
whale = Player(334, 650, 128, 128)  # Spawns the Player at the start of the game in the middle of the screen
speedboat_locations = (125, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800)
speedboats = []
beams = []
cooldown = 0
wave_1 = 10

while game:

    for event in pygame.event.get():  # this for-loop makes sure the game exits when clicking x
        if event.type == pygame.QUIT:
            game = False

    # Basic cooldown for the projectiles of the player
    if cooldown > 0:
        cooldown += 1
    if cooldown > 50:
        cooldown = 0

    for beam in beams:
        for speedboat in speedboats:
            if speedboat.alive:
                if beam.y - beam.width < speedboat.hitbox[1] + speedboat.hitbox[3] and beam.y + beam.width > \
                        speedboat.hitbox[1]:
                    if beam.x + beam.height > speedboat.hitbox[0] and beam.x - beam.height < speedboat.hitbox[0] + speedboat.hitbox[2]:
                        speedboat.hit()
                        beams.pop(beams.index(beam))
        if beam.y > 0:
            beam.y -= beam.speed  # This makes sure the bullet moves forward as long as it is not of the screen
        else:
            beams.pop(beams.index(beam))  # If the bullet goes of the screen it gets removed from the list

    # --- PLAYER CONTROLS ---
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and whale.x > whale.mov_speed:
        # Makes sure the whale can move left
        # and prevents the whale from exiting the screen
        whale.x = whale.x - whale.mov_speed

    if keys[pygame.K_RIGHT] and whale.x < 800 - whale.mov_speed - whale.width:
        # Makes sure the whale can move right
        # and prevents the whale from exiting the screen
        whale.x = whale.x + whale.mov_speed

    if keys[pygame.K_SPACE] and cooldown == 0:
        # This block of code takes care of the beam-projectile the player can shoot
        if len(beams) < 3:
            beams.append(
                Projectile(round(whale.x + (whale.width // 2) - (32 // 2)), round(whale.y - (32 // 2)), 32, 32, 2,
                           beam_sprite))
            # The beam gets spawned at the whale X/Y Coordinate. To make the beam appear in the middle and at the
            # nose we add half the sprites width - half the width of the projectile to the for the x coordinate
            # and we use the y coordinate - half the length of the projectile to make the attack spawn at the top
        cooldown = 1

    # --- ENEMY SPAWNING ---
    # This block of code spawns the first wave of enemies
    for n in range(wave_1):
        speedboats.append(Enemy(random.randint(64, 734), random.randrange(-1000, -100), 64, 64, 1, speedboat_sprite))
        wave_1 -= 1
    

    redrawGameWindow()

pygame.quit()
