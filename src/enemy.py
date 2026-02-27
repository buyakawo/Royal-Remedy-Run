import pygame

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Load all the frames for the animation
        self.frames = [
            pygame.image.load(f'assets/images/ws{i}.png') for i in range(1, 6)
        ]
        # Scale all frames to the desired size
        self.frames = [pygame.transform.scale(frame, (80, 60)) for frame in self.frames]

        self.current_frame = 0  # Track the current frame
        self.image = self.frames[self.current_frame]  # Set the initial image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.animation_counter = 0  # Counter to control the speed of animation
        self.animation_speed = 10  # Adjust this value for animation speed

    def update(self):
        # Update animation every few frames
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # Cycle through frames
            self.image = self.frames[self.current_frame]  # Update the displayed image


