import pygame
from constants import PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, groups):
        super().__init__(groups)
        self.position = pygame.Vector2(x, y)
        self.direction = pygame.Vector2()
        self.radius = radius
        self.speed = PLAYER_SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)
