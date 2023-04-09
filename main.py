import pygame
from dcr import views
from dcr import models
from dcr.consts import params, colors

def setup():
    pygame.init()

    return pygame.display.set_mode((params.SCREEN_X, params.SCREEN_Y), 0)

def run(screen):
    sprite = views.CircleSprite(screen)
    circle = models.Circle(sprite)

    # Game loop
    while True:
        # Calculate rules
        circle.move()

        # Draw
        screen.fill(colors.BLACK)
        circle.draw()
        pygame.display.update()
        pygame.time.delay(10)

        # Events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()

if __name__ == '__main__':
    main_screen = setup()
    run(main_screen)