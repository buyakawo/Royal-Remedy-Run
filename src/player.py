import pygame
from pygame.locals import *
import globals

# -------------------- Initialization ----------------------
screen = pygame.display.set_mode((globals.screen_width, globals.screen_height))
font = pygame.font.SysFont('Bauhaus 93', 70)
blue = (0, 0, 255)


# -------------------- Player Class ----------------------
class Player():
    def __init__(self, x, y, blob_group, lava_group, exit_group, remedy_group, jump_fx, game_over_fx):
        self.reset(x, y, blob_group, lava_group, exit_group, remedy_group, jump_fx, game_over_fx)

    # Update Function for the player
    def update(self, world):
        dx = 0
        dy = 0
        walk_cooldown = 5
        game_over = globals.game_over
        col_thresh = 20

        # Update logic only if the game is not over
        if globals.game_over == 0:
            # Keyboard control
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.jump_fx.play()
                self.vel_y = -20
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 2
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 2
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Player's Animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Player's Gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Collision Dtection
            self.in_air = True
            for tile in world.tile_list:
                # Check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # Collision detection  with enemies
            if pygame.sprite.spritecollide(self, self.blob_group, False):
                if globals.player_lives > 0:  # Reduce lives only if greater than 0
                    globals.player_lives -= 1
                    if globals.player_lives <= 0:
                        self.game_over_fx.play()
                        globals.game_over = -1  # Trigger game over
                    else:
                        # Reset player position and other necessary states for respawn
                        self.reset(100, globals.screen_height - 130, self.blob_group, self.lava_group, self.exit_group, self.remedy_group, self.jump_fx, self.game_over_fx)
                return globals.game_over  # Return current game state


            # Collision detection with lava
            if pygame.sprite.spritecollide(self, self.lava_group, False):
                if globals.player_lives > 0:  # Reduce lives if greater than 0
                    globals.player_lives -= 1
                    if globals.player_lives <= 0:
                        self.game_over_fx.play()
                        globals.game_over = -1  # Trigger game over
                    else:
                        # Reset player position and other necessary states for respawn
                        self.reset(100, globals.screen_height - 130, self.blob_group, self.lava_group, self.exit_group, self.remedy_group, self.jump_fx, self.game_over_fx)
                return globals.game_over  # Return current game state

            # Collision detection with remedy
            if pygame.sprite.spritecollide(self, self.remedy_group, True):
                globals.game_over = 2  # New state indicating the player has won


            # Collision detection with gate
            if pygame.sprite.spritecollide(self, self.exit_group, False):
                return 1

            # Update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            # Prevent player from falling off the bottom of the screen
            if self.rect.bottom > globals.screen_height:
                self.rect.bottom = globals.screen_height
                dy = 0

        elif globals.game_over == -1:
            self.image = self.dead_image
            self.rect.y -=5

        # Draw the player on the screen
        screen.blit(self.image, self.rect)

        return game_over

    # Reset function for the player
    def reset(self, x, y, blob_group, lava_group, exit_group, remedy_group, jump_fx, game_over_fx):
        # Animation list
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        # Player (princess)
        for num in range(0, 4):
            img_left = pygame.image.load(f'assets/images/g{num}.png')
            img_left = pygame.transform.scale(img_left, (50, 100))
            img_right = pygame.transform.flip(img_left, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        # Initialization
        self.dead_image = pygame.image.load('assets/images/dead.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (40, 80))
        self.image = self.images_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.blob_group = blob_group
        self.lava_group = lava_group
        self.exit_group = exit_group
        self.remedy_group = remedy_group
        self.jump_fx = jump_fx
        self.game_over_fx= game_over_fx

