# Example file showing a circle moving on screen
import pygame
from player import Player
from enemy import Enemy

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
game_over = False

# Load all player sprite frames
player_images = []
for i in range(1, 9):
    img = pygame.image.load(f"sprites/green_virus/Green{i}.png")
    player_images.append(img)

# Load all enemy sprite frames
enemy_images = []
for i in range(1, 9):
    img = pygame.image.load(f"sprites/blue_virus/Blue{i}.png")
    enemy_images.append(img)

# Define player stats
move_speed = 200

# Create player and sprite group
player = Player(player_images, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), move_speed)
sprites = pygame.sprite.Group()
sprites.add(player)

# Create multiple enemies
enemies = []
enemy_positions = [(200, 100), (400, 150), (600, 200)]
for pos in enemy_positions:
    enemy = Enemy(enemy_images, pygame.Vector2(pos[0], pos[1]), 100, screen.get_width(), screen.get_height())
    enemies.append(enemy)
    sprites.add(enemy)

# Game variables
score = 0
font = pygame.font.Font(None, 36)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                # Restart game
                game_over = False
                score = 0
                player.health = player.max_health
                player.bullets = []
                enemies.clear()
                for pos in enemy_positions:
                    enemy = Enemy(enemy_images, pygame.Vector2(pos[0], pos[1]), 100, screen.get_width(), screen.get_height())
                    enemies.append(enemy)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    if not game_over:
        # Update and draw player
        keys = pygame.key.get_pressed()
        player.update(dt, keys)
        
        # Update all enemies
        for enemy in enemies:
            enemy.update(dt)
            enemy.update_bullets(dt)
            enemy.shoot_at_player(player.rect.center)
        
        sprites.draw(screen)
        
        # Draw player bullets
        for bullet in player.bullets:
            screen.blit(bullet.image, bullet.rect)
        
        # Draw enemy bullets
        for enemy in enemies:
            for bullet in enemy.bullets:
                screen.blit(bullet.image, bullet.rect)
        
        # Check for player bullet-enemy collisions
        for bullet in player.bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= 10
                    if bullet in player.bullets:
                        player.bullets.remove(bullet)
                    if enemy.health <= 0:
                        score += 1
                        enemy.kill()
                        if enemy in enemies:
                            enemies.remove(enemy)
                    break
        
        # Check for enemy bullet-player collisions
        for enemy in enemies:
            for bullet in enemy.bullets[:]:
                if bullet.rect.colliderect(player.rect):
                    player.health -= 10
                    if bullet in enemy.bullets:
                        enemy.bullets.remove(bullet)
                    if player.health <= 0:
                        game_over = True
        
        # Draw health bars for enemies
        for enemy in enemies:
            health_percent = max(0, enemy.health / enemy.max_health)
            bar_width = 100
            bar_height = 10
            bar_x = enemy.rect.centerx - bar_width // 2
            bar_y = enemy.rect.top - 20
            
            # Red background bar
            pygame.draw.rect(screen, "red", (bar_x, bar_y, bar_width, bar_height))
            # Green health bar
            pygame.draw.rect(screen, "green", (bar_x, bar_y, bar_width * health_percent, bar_height))
            # White border
            pygame.draw.rect(screen, "white", (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw player health bar at top
        player_health_percent = max(0, player.health / player.max_health)
        player_bar_width = 200
        player_bar_height = 20
        player_bar_x = 10
        player_bar_y = 10
        
        pygame.draw.rect(screen, "red", (player_bar_x, player_bar_y, player_bar_width, player_bar_height))
        pygame.draw.rect(screen, "green", (player_bar_x, player_bar_y, player_bar_width * player_health_percent, player_bar_height))
        pygame.draw.rect(screen, "white", (player_bar_x, player_bar_y, player_bar_width, player_bar_height), 2)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (screen.get_width() - 200, 10))
    else:
        # Game over screen
        game_over_text = font.render("GAME OVER", True, "red")
        restart_text = font.render("Press SPACE to restart", True, "white")
        score_text = font.render(f"Final Score: {score}", True, "white")
        
        screen.blit(game_over_text, (screen.get_width() // 2 - 150, screen.get_height() // 2 - 100))
        screen.blit(score_text, (screen.get_width() // 2 - 150, screen.get_height() // 2))
        screen.blit(restart_text, (screen.get_width() // 2 - 200, screen.get_height() // 2 + 100))

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()