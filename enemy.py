import pygame
import random
from enemy_bullet import EnemyBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, images, pos, speed, width, height):
        super().__init__()
        self.images = images
        self.frame = 0  
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.width = width
        self.height = height
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)
        self.direction_change_timer = 0
        self.health = 100
        self.max_health = 100
        self.bullets = []
        self.shoot_cooldown = 0

    def update(self, dt):
        # Change direction randomly every 60 frames (1 second at 60 FPS)
        self.direction_change_timer += 1
        if self.direction_change_timer > 60:
            self.velocity_x = random.uniform(-1, 1)
            self.velocity_y = random.uniform(-1, 1)
            self.direction_change_timer = 0
        
        # Normalize velocity and apply speed
        magnitude = (self.velocity_x**2 + self.velocity_y**2)**0.5
        if magnitude > 0:
            self.velocity_x /= magnitude
            self.velocity_y /= magnitude
        
        # Move enemy
        self.rect.x += self.velocity_x * self.speed * dt
        self.rect.y += self.velocity_y * self.speed * dt
        
        # Keep enemy within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
        
        # Animate sprite frames
        self.frame += 0.2
        self.image = self.images[int(self.frame) % len(self.images)]

    def shoot_at_player(self, player_pos):
        if self.shoot_cooldown <= 0:
            # Calculate direction to player
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 0:
                # Normalize direction
                direction = (dx / distance, dy / distance)
                bullet = EnemyBullet(self.rect.center, direction, 300)
                self.bullets.append(bullet)
                self.shoot_cooldown = 1.5  # 1.5 second cooldown between enemy shots
    
    def update_bullets(self, dt):
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.lifetime <= 0:
                self.bullets.remove(bullet)
        
        self.shoot_cooldown = max(0, self.shoot_cooldown - dt)