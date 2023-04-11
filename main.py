import pygame
from dcr import views
from dcr import models
from dcr.consts import params, colors

def setup():
    pygame.init()

    display = pygame.display.set_mode((params.SCREEN_X, params.SCREEN_Y), 0)
    font = pygame.font.SysFont('arial', 14, False, False)

    setup_data = {
        'display': display,
        'font': font
    }

    return setup_data

def run(screen, font):
    ui_view = views.BaseUIView(screen, font)
    base_ui = models.BaseUI(ui_view)
    sprite = views.CardSprite(screen, font)
    card_1 = models.DigimonCard(base_ui, 'Card', 'Brown', sprite, 'This is a test card', 15, 14)
    card_2 = models.DigimonCard(base_ui, 'Card', 'Brown', sprite, 'This is another test card', 8, 12)
    card_3 = models.DigimonCard(base_ui, 'Card', 'Brown', sprite, 'This is another test card', 1, 3)
    card_4 = models.DigimonCard(base_ui, 'Card', 'Brown', sprite, 'This is another test card', 5, 2)
    cards = (card_1, card_2, card_3, card_4)

    # Game loop
    while True:
        # Calculate rules
        

        # Draw
        screen.fill(colors.BLACK)
        base_ui.draw()
        card_x = 2
        card_y = 2
        for card in cards:
            card.draw(card_x, card_y)
            card_x += card.sprite.width + 2
        
        pygame.display.update()
        pygame.time.delay(10)

        # Events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            for card in cards:
                card.process_events(e)

if __name__ == '__main__':
    main_screen = setup()
    run(main_screen['display'], main_screen['font'])