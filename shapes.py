import pygame
from constants import *

class Shape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, groups):
        super().__init__(groups)
        self.position = pygame.Vector2(x, y)
        self.direction = pygame.Vector2()
        self.radius = radius

    #dummy methods should get overridden
    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def collides(self, Shape):
        other = Shape
        distance = pygame.Vector2.distance_to(self.position, other.position)
        if distance <= self.radius + other.radius:
            return True
        else:
            return False
        

class Player(Shape):
    def __init__(self, x, y, radius, groups):
        super().__init__(x, y, radius, groups)
        self.radius = radius
        self.speed = PLAYER_SPEED
        self.cooldown = PLAYER_SHOT_COOLDOWN

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.position += self.direction * self.speed * dt
        #constrain
        if self.position.x < 0:
            self.position.x = 0
        if self.position.x > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH
        if self.position.y < 0:
            self.position.y = 0
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT

    def update(self, dt):
        self.input()
        self.move(dt)


class Enemy(Shape):
    def __init__(self, x, y, radius, player, groups):
        super().__init__(x, y, radius, groups)
        self.speed = ENEMY_SPEED
        self.player = player

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 4)

    def move(self, dt):
        self.direction = (self.player.position - self.position).normalize()

        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def update(self, dt):
        self.move(dt)

class Bullet(Shape):
    def __init__(self, x, y, radius, speed, direction, groups):
        super().__init__(x, y, radius, groups)
        self.speed = speed
        self.direction = pygame.Vector2(direction)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "light blue", self.position, self.radius, 1)

    def move(self, dt):
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def update(self, dt):
        #destroy if offscreen
        if self.position.y < 0 or self.position.y > SCREEN_HEIGHT or self.position.x < 0 or self.position.x > SCREEN_WIDTH:
            self.kill()

        self.move(dt)