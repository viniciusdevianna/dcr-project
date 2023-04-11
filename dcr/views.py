from pygame import draw, image
from .consts import params, colors

class BaseUIView():
    def __init__(self, surface, font) -> None:
        self.surface = surface
        self.font = font
        self.show_description = False
        self.description = None

    def draw(self): 
        if self.show_description:
            self._draw_description()

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

        return frame
