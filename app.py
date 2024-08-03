import pygame
import math
import random

pygame.init()

# initialize app parameters
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
running = True

# the title of this application
pygame.display.set_caption("youtube shorts-esque ball collision simulator")

# future sound for clicks
click_sound = pygame.mixer.Sound("click.wav")


# ball parameters
ball_radius = 20

BALL_COLOR = (255, 0, 0)
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.acceleration = 0.5
        self.max_speed = 10
        self.friction = 0.98

    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        # Apply friction
        self.dx *= self.friction
        self.dy *= self.friction
        
        # Keep ball within screen bounds
        self.x = max(ball_radius, min(width - ball_radius, self.x))
        self.y = max(ball_radius, min(height - ball_radius, self.y))

    def apply_force(self, force_x, force_y):
        self.dx += force_x * self.acceleration
        self.dy += force_y * self.acceleration
        
        # Limit speed
        speed = math.sqrt(self.dx**2 + self.dy**2)
        if speed > self.max_speed:
            self.dx = (self.dx / speed) * self.max_speed
            self.dy = (self.dy / speed) * self.max_speed

    def draw(self):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), ball_radius)

# Create the ball
ball = Ball(width // 2, height // 2)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # Handle input
    keys = pygame.key.get_pressed()
    force_x = force_y = 0
    if keys[pygame.K_a]: force_x -= 1
    if keys[pygame.K_d]: force_x += 1
    if keys[pygame.K_w]: force_y -= 1
    if keys[pygame.K_s]: force_y += 1

    # Apply force and move the ball
    ball.apply_force(force_x, force_y)
    ball.move()
    ball.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(60)

pygame.quit()