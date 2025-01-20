import sys
import pygame
from constants import *
from shot import Shot

pygame.mixer.init()

from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player =  Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    game = True
    while game:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return
        
        for object in updatable:
            object.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()

        screen.fill("black")

        for object in drawable:
            object.draw(screen)

        pygame.display.flip()
            
        # limit fps to 60 
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()