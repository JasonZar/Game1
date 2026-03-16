import pygame

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.speed = speed
        self.lifetime = 5  # seconds before bullet disappears

    def update(self, dt):
        # Move bullet in direction
        self.rect.x += self.direction[0] * self.speed * dt
        self.rect.y += self.direction[1] * self.speed * dt
        
        # Decrease lifetime
        self.lifetime -= dt
