import pygame
import random
from dcr import views
from dcr import models
from dcr import statemachine
from dcr.consts import params, colors

def setup():
    pygame.init()

    display = pygame.display.set_mode((params.SCREEN_X, params.SCREEN_Y), 0)
    font = pygame.font.SysFont('arial', 14, False, False)
    sm = statemachine.StateMachine()

    setup_data = {
        'screen': display,
        'font': font,
        'statemachine': sm
    }

    return setup_data

def run(screen, font, statemachine):
    player = models.Player('Jogador')
    opponent = models.Player('Oponente')
    ui_view = views.BaseUIView(screen, font)
    base_ui = models.BaseUI(ui_view, statemachine, player, opponent)
    sprite = views.CardSprite(screen, font)
    base_ui.initial_load(sprite)
    statemachine.draw_phase()

    # Game loop
    while True:
        # Calculate rules
        base_ui.calculate_rules()

        # Draw
        screen.fill(colors.BLACK)
        base_ui.draw()       
        pygame.display.update()
        pygame.time.delay(10)

        # Events
        events = pygame.event.get()
        base_ui.process_events(events)            
            

if __name__ == '__main__':
    main_screen = setup()
    run(**main_screen)