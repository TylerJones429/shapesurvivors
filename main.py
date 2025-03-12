import pygame
from constants import *
from shapes import *
from random import randint

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0
shot_direction = pygame.Vector2(1,0)
shot_cooldown = PLAYER_SHOT_COOLDOWN
enemy_waves = 6
wave_timer = 0
distance_to_enemies = {}

font = pygame.font.Font(None, 60)

def display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, 'white')
    text_rect = text_surf.get_frect(midbottom = (SCREEN_WIDTH/2,50))
    screen.blit(text_surf, text_rect)

updateable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS, (updateable, drawable))
# for enemy in range(10):
#     enemy = Enemy(randint(0, SCREEN_WIDTH), randint(-200, -20), ENEMY_RADIUS, player, (updateable, drawable, enemies))
# enemy_waves -= 1

running = True
#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for obj in updateable:
        obj.update(dt)

    #spawn enemies
    if enemy_waves > 0:
        wave_timer -= dt
        if wave_timer <= 0:
            enemy_waves -= 1
            wave_timer = ENEMY_WAVE_TIMER
            for enemy in range(ENEMY_COUNT):
                enemy = Enemy(randint(0, SCREEN_WIDTH), randint(-200, -20), ENEMY_RADIUS, player, (updateable, drawable, enemies))

    shot_cooldown -= dt
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
                    break

    if enemies:
        for enemy in enemies:
            if enemy.collides(player):
                player.damage()
                if player.health <= 0:
                    print("Game Over!")
                    running = False
                    break

    if enemy_waves == 0 and len(enemies) == 0:
        print("You win!")
        running = False
        break      

    screen.fill('black')

    for obj in drawable:
        obj.draw(screen)

    display_score()

    pygame.display.update()

    dt = clock.tick(60) / 1000
