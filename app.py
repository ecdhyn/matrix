import pygame
import math
import random

pygame.init()

# initialize app parameters
width, height = 1600, 1000
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

# the title of this application
pygame.display.set_caption("let's bounce")

background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (width, height))

# sound for clicks
click_sound = pygame.mixer.Sound("click.wav")

# ball parameters
ball_radius = 20
BALL_COLOR1 = (255, 255, 255)
BALL_COLOR2 = (255, 255, 255) 

class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.acceleration = 0.5
        self.max_speed = 30
        self.friction = 0.98
        self.color = color

    def move(self):
        next_x = self.x + self.dx
        next_y = self.y + self.dy
        
        if next_x < ball_radius or next_x > width - ball_radius:
            self.dx = -self.dx
            click_sound.play()
        if next_y < ball_radius or next_y > height - ball_radius:
            self.dy = -self.dy
            click_sound.play()
        
        self.x += self.dx
        self.y += self.dy
        
        self.dx *= self.friction
        self.dy *= self.friction
        
        self.x = max(ball_radius, min(width - ball_radius, self.x))
        self.y = max(ball_radius, min(height - ball_radius, self.y))

    def apply_force(self, force_x, force_y):
        self.dx += force_x * self.acceleration
        self.dy += force_y * self.acceleration
        
        speed = math.sqrt(self.dx**2 + self.dy**2)
        if speed > self.max_speed:
            self.dx = (self.dx / speed) * self.max_speed
            self.dy = (self.dy / speed) * self.max_speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), ball_radius)

def check_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < 2 * ball_radius:
        # collision detected, calculate new velocities
        angle = math.atan2(dy, dx)
        sin = math.sin(angle)
        cos = math.cos(angle)
        
        # rotate velocities
        vx1 = ball1.dx * cos + ball1.dy * sin
        vy1 = ball1.dy * cos - ball1.dx * sin
        vx2 = ball2.dx * cos + ball2.dy * sin
        vy2 = ball2.dy * cos - ball2.dx * sin
        
        # swap x velocities
        vx1, vx2 = vx2, vx1
        
        # rotate velocities back
        ball1.dx = vx1 * cos - vy1 * sin
        ball1.dy = vy1 * cos + vx1 * sin
        ball2.dx = vx2 * cos - vy2 * sin
        ball2.dy = vy2 * cos + vx2 * sin
        
        # move balls apart to prevent sticking
        overlap = 2 * ball_radius - distance
        ball1.x -= overlap * 0.5 * cos
        ball1.y -= overlap * 0.5 * sin
        ball2.x += overlap * 0.5 * cos
        ball2.y += overlap * 0.5 * sin
        
        click_sound.play()

# create the balls
ball1 = Ball(width // 3, height // 2, BALL_COLOR1)
ball2 = Ball(2 * width // 3, height // 2, BALL_COLOR2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    # handle input for ball 1 (WASD)
    keys = pygame.key.get_pressed()
    force_x1 = force_y1 = 0
    if keys[pygame.K_a]: force_x1 -= 1
    if keys[pygame.K_d]: force_x1 += 1
    if keys[pygame.K_w]: force_y1 -= 1
    if keys[pygame.K_s]: force_y1 += 1

    # handle input for ball 2 (Arrow keys)
    force_x2 = force_y2 = 0
    if keys[pygame.K_LEFT]: force_x2 -= 1
    if keys[pygame.K_RIGHT]: force_x2 += 1
    if keys[pygame.K_UP]: force_y2 -= 1
    if keys[pygame.K_DOWN]: force_y2 += 1

    # apply forces and move balls
    ball1.apply_force(force_x1, force_y1)
    ball2.apply_force(force_x2, force_y2)
    ball1.move()
    ball2.move()

    # check for collision between balls
    check_collision(ball1, ball2)

    # draw balls
    ball1.draw()
    ball2.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()