import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, images, pos, speed):
        super().__init__()
        self.images = images
        self.frame = 0  
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.bullets = []
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = 100

    def shoot(self, direction):
        if self.shoot_cooldown <= 0:
            bullet = Bullet(self.rect.center, direction, 400)
            self.bullets.append(bullet)
            self.shoot_cooldown = 0.2  # 200ms cooldown between shots

    def update(self, dt, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed * dt
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt
        
        # Shoot in direction of arrow keys
        if keys[pygame.K_UP]:
            self.shoot((0, -1))
        elif keys[pygame.K_DOWN]:
            self.shoot((0, 1))
        elif keys[pygame.K_LEFT]:
            self.shoot((-1, 0))
        elif keys[pygame.K_RIGHT]:
            self.shoot((1, 0))

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.lifetime <= 0:
                self.bullets.remove(bullet)
        
        # Update shoot cooldown
        self.shoot_cooldown -= dt

        self.frame += 0.2
        self.image = self.images[int(self.frame) % len(self.images)]