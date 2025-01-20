import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED, SHOT_RADIUS
from shot import Shot


class Player(CircleShape):
    shoot_sound = pygame.mixer.Sound("./assets/sound/retro-laser.mp3")
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            self.shoot()
            
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation) * self.radius / 1.5

        # define the vertices
        tip = self.position + forward * self.radius
        base_left = self.position - forward * (self.radius / 2) + right
        base_right = self.position - forward * (self.radius / 2) - right

        return [tip, base_left, base_right]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot_start_pos = self.position + forward * (self.radius + SHOT_RADIUS)

        shot = Shot(shot_start_pos.x, shot_start_pos.y)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        
        Player.shoot_sound.play()