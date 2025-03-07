import pygame
from constants import *
from shapes import *
from random import randint

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS, (updateable, drawable))
    for enemy in range(10):
        enemy = Enemy(randint(0, SCREEN_WIDTH), randint(-200, -20), ENEMY_RADIUS, player, (updateable, drawable, enemies))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        for obj in updateable:
            obj.update(dt)

        screen.fill('black')

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()