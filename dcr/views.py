from pygame import draw, image
from .consts import params, colors, states

class BaseUIView():
    def __init__(self, surface, font) -> None:
        self.surface = surface
        self.font = font
        self.show_description = False
        self.description = None
        self.confirm_button_view = ButtonSprite(self.surface, self.font, params.SCREEN_X - 60, params.SCREEN_Y - 40)

    def draw(self, state, player, opponent):
        if state == states.States.SUMMONING:
            card_x = 2
            card_y = 2
            for card in player.hand:
                card.draw(card_x, card_y)
                card_x += card.sprite.width + 2

            self.confirm_button_view.draw()
            
            if self.show_description:
                self._draw_description()
        
        if state == states.States.BATTLING:
            self.surface.fill(colors.BLACK)
            print(f'{player.total_power} / {player.total_health} x {opponent.total_power} / {opponent.total_health}')

    def _draw_description(self):
        height = 50
        width = params.SCREEN_X
        draw.rect(self.surface, colors.WHITE_TRANSPARENT, (0, params.SCREEN_Y - height, width, height), 0)

        if self.description is None:
            text = ''
        else:
            text = self.description
        description_img = self.font.render(text, True, colors.BLACK)
        description_x = 5
        description_y = params.SCREEN_Y - height + 5
        self.surface.blit(description_img, (description_x, description_y))

class CardSprite():
    def __init__(self, surface, font, image='no-image.jpg') -> None:
        self.surface = surface
        self.font = font
        self.image = f'{params.CARDS_IMG_DIR}\\{image}'
        self.width = 100
        self.height = 150
        self.frame = None

    def draw(self, left, top, selected, power=None, health=None):
        # Draw card frame
        frame = draw.rect(self.surface, colors.WHITE_TRANSPARENT, (left, top, self.width, self.height), 0)

        # Draw card img
        img = image.load(self.image)
        self.surface.blit(img, (left + 2, top + 2))

        # Draw card power and health if digimon card
        if power is not None and health is not None:
            ph_text = f'{power} / {health}'
            ph_img = self.font.render(ph_text, True, colors.BLACK)
            ph_x = left + self.width - ph_img.get_width() - 5
            ph_y = top + self.height - ph_img.get_height() - 5
            self.surface.blit(ph_img, (ph_x, ph_y))

        if selected:
            draw.rect(self.surface, colors.SELECTED, (left, top, self.width, self.height), 2)

        self.frame = frame
    
class ButtonSprite():
    def __init__(self, surface, font, left, top, width=50, height=30, color=colors.PRIMARY, text='Confirmar') -> None:
        self.surface = surface
        self.font = font
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.frame = None

    def draw(self):
        frame = draw.rect(self.surface, self.color, (self.left, self.top, self.width, self.height), 0)
        btn_text = self.font.render(self.text, True, colors.WHITE)
        btn_text_x = self.left + 5
        btn_text_y = self.top + 5
        self.surface.blit(btn_text, (btn_text_x, btn_text_y))

        self.frame = frame
