import pygame
import random

# Initialize game window here
pygame.init()

# Variables for the game window
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Sea Invaders')
clock = pygame.time.Clock()  # Adds the clock for spawn timers
message_font = pygame.font.SysFont('Calibri', 36)

# Sprites, background and music
background = pygame.image.load('Background.jpg')
whale_sprite = pygame.image.load('Whale.png')
speedboat_sprite = pygame.image.load('Speedboat.png')
beam_sprite = pygame.image.load('Beam.png')
life_sprite = pygame.image.load('Life.png')
pirate_boss_sprite_right = pygame.image.load('Pirateboss_right.png')


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
        # Whale hitbox check
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, width, height, mov_speed):
        # Variables for the various enemies
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.mov_speed = mov_speed
        self.image = speedboat_sprite
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(64, 734)
        self.rect.y = random.randrange(-150, -100)
        self.hitbox = (self.rect.x + 22, self.rect.y + 15, 19, 45)
        self.alive = True

    def update(self):
        # This function lets the enemy go forward until the end of the screen
        max_distance = 800 - self.height
        if self.rect.y < max_distance:
            self.rect.y += self.mov_speed

    def hit(self):
        # This function deletes the sprite from the sprite group when hit by an attack from a player
        self.kill()
        self.alive = False


class Boss():
    def __init__(self, x, y, width, height, mov_speed, hitpoints):
        # Variables for the boss objects
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mov_speed = mov_speed
        self.hitpoints = hitpoints
        self.hitbox = (self.x + 30, self.y + 50, 225, 160)  # Dimensions of the hitbox to make it close to the model
        self.alive = False
        self.killed = False
        self.end_reached = False

    def draw(self, window):
        if self.alive and not self.killed:
            window.blit(pirate_boss_sprite_right, (self.x, self.y))
            self.hitbox = (self.x + 30, self.y + 50, 225, 160)
            pygame.draw.rect(window, (255, 0, 0),
                             (self.x + ((self.width / 2) - (self.hitpoints / 2)), self.y + 220, 50, 10))
            pygame.draw.rect(window, (0, 255, 0),
                             (self.x + ((self.width / 2) - (self.hitpoints / 2)), self.y + 220, self.hitpoints, 10))

            # Pirate Boss hitbox check
            # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def move(self):
        # This function moves the boss forward. As soon as the boss reaches the end it spawns lower on the screen.
        # If the end is reached the model is deleted and the end_reached parameter is set tot True.
        max_distance = 800 - self.height
        if self.x < (800 + self.width):
            self.x += self.mov_speed

        else:
            self.y += 100
            self.x = -51

        if self.y >= max_distance:
            self.alive = False
            self.end_reached = True

    def hit(self):
        # As soon as the Whale hitpoints reaches 0, the model is overwritten on screen.
        if self.hitpoints <= 0:
            self.killed = True
            return True


class Projectile():
    def __init__(self, x, y, width, height, speed, damage, image):
        # Variables for the player attacks (ranged)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.damage = damage
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def checkCollision(self, enemy):
        # This function checks collision with enemies that belong to a Sprite Group.
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # noinspection PyTypeChecker
        return any(pygame.sprite.spritecollide(self, enemy, True))


class Hud():
    # class to place the HUDS on the screen (lives, score)
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))


# Methods
def redrawGameWindow():
    window.blit(background, (0, 0))  # Loads in the background
    whale.draw(window)  # Draws the Whale in the game
    scoreboard = message_font.render(str(score), True, (255, 255, 255))
    window.blit(scoreboard, (700, 760))

    x_life = 0
    # This for loop places the lives next to eachother on the HUD
    for life in range(lives):
        life = Hud(x_life, 760, life_sprite)
        x_life += 25
        life.draw(window)

    if lives == 0:
        text = f'Game over! Your score: {score}.'
        game_over = message_font.render(text, True, (0, 0, 0))
        window.blit(game_over, (200, 200))

    if score >= 75:
        pirate_boss.alive = True
        pirate_boss.draw(window)
        pirate_boss.move()

    speedboats.draw(window)
    speedboats.update()

    for fired_beam in beams:
        fired_beam.draw(window)

    pygame.display.update()  # This updates the above changes to the game window


# Game logic here
game = True
whale = Player(334, 650, 128, 128)  # Spawns the Player at the start of the game in the middle of the screen
speedboat_locations = (125, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800)
speedboats = pygame.sprite.Group()
pirate_boss = Boss(1, 1, 256, 256, 1, 50)
beams = []
cooldown = 0
lives = 3
score = 0
multiplier = 1
start = pygame.time.get_ticks()

while game:

    for event in pygame.event.get():  # this for-loop makes sure the game exits when clicking x
        if event.type == pygame.QUIT:
            game = False

    # Life check
    for speedboat in speedboats:
        if speedboat.rect.y >= 734:
            speedboat.kill()
            lives -= 1

        if not speedboat.alive:
            speedboats.remove(speedboat)

    if pirate_boss.end_reached and not pirate_boss.killed:
        lives = 0

    # Basic cooldown for the projectiles of the player
    if cooldown > 0:
        cooldown += 1
    if cooldown > 50:
        cooldown = 0

    # Collision of attacks
    for beam in beams:
        if beam.checkCollision(speedboats):
            score += (25 * multiplier)
            beams.pop(beams.index(beam))
        if pirate_boss.alive and not pirate_boss.killed:
            if beam.y - beam.width < pirate_boss.hitbox[1] + pirate_boss.hitbox[3] and beam.y + beam.width > \
                    pirate_boss.hitbox[1]:
                if beam.x + beam.height > pirate_boss.hitbox[0] and beam.x - beam.height < pirate_boss.hitbox[0] + \
                        pirate_boss.hitbox[2]:
                    pirate_boss.hitpoints -= beam.damage
                    beams.pop(beams.index(beam))
                    alive_check = pirate_boss.hit()
                    if alive_check:
                        multiplier += 1

        if beam.y > 0:
            beam.y -= beam.speed  # This makes sure the bullet moves forward as long as it is not of the screen
            beam.rect.center = (beam.x, beam.y)
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
                           10, beam_sprite))
            # The beam gets spawned at the whale X/Y Coordinate. To make the beam appear in the middle and at the
            # nose we add half the sprites width - half the width of the projectile to the for the x coordinate
            # and we use the y coordinate - half the length of the projectile to make the attack spawn at the top
        cooldown = 1

    # --- ENEMY SPAWNING ---

    now = pygame.time.get_ticks()
    spawn_time = 3000
    speedboat = Enemy(64, 64, 1)

    # Game loop to increase difficulty
    if score > 500:
        spawn_time = 2000

    if score > 1000:
        spawn_time = 1000

    if score > 5000:
        speedboat = Enemy(64, 64, 2)
        spawn_time = 2000

    if now - start > spawn_time:
        start = now
        speedboats.add(speedboat)







    redrawGameWindow()

pygame.quit()
