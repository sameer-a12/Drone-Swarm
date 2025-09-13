import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Swarm - Separation Rule")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_DRONES = 30
SEPARATION_DISTANCE = 50
MAX_SPEED = 3

class Drone:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        self.velocity.scale_to_length(random.uniform(1, MAX_SPEED))
        self.radius = 6

    def update(self, drones):
        self.separate(drones)
        self.pos += self.velocity
        self.wrap_around_screen()

    def separate(self, drones):
        steer = pygame.math.Vector2()
        total = 0

        for other in drones:
            if other is self:
                continue
            distance = self.pos.distance_to(other.pos)
            if distance < SEPARATION_DISTANCE and distance > 0:
                diff = self.pos - other.pos
                diff /= distance
                steer += diff
                total += 1
        if total > 0:
            steer /= total
            self.velocity += steer
            if self.velocity.length() > MAX_SPEED:
                self.velocity.scale_to_length(MAX_SPEED)

    def wrap_around_screen(self):
        if self.pos.x < 0:
            self.pos.x = WIDTH
        elif self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        elif self.pos.y > HEIGHT:
            self.pos.y = 0

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, self.pos, self.radius)

drones = []
for _ in range(NUM_DRONES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    drones.append(Drone(x, y))

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for drone in drones:
        drone.update(drones)
        drone.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
