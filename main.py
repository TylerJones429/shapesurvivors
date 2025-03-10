import pygame
from constants import *
from shapes import *
from random import randint

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    shot_direction = pygame.Vector2(1,0)
    shot_cooldown = PLAYER_SHOT_COOLDOWN
    distance_to_enemies = {}

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

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

        shot_cooldown -= 1 * dt
        if shot_cooldown <= 0 and enemies:
            #find distances to all enemies
            distance_to_enemies.clear()
            for enemy in enemies:
                distance = pygame.Vector2.distance_to(player.position, enemy.position)
                distance_to_enemies[distance] = enemy.position
            #fire at location of nearest enemy
            nearest = min(distance_to_enemies)
            bullet_direction = (distance_to_enemies[nearest] - player.position).normalize()
            bullet = Bullet(player.position.x, player.position.y, BULLET_RADIUS, BULLET_SPEED, bullet_direction, (updateable, drawable, bullets))
            shot_cooldown = PLAYER_SHOT_COOLDOWN
        
        #collision
        if bullets:
            for bullet in bullets:
                for enemy in enemies:
                    if bullet.collides(enemy):
                        bullet.kill()
                        enemy.kill()

        screen.fill('black')

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()