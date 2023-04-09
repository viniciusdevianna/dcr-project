from pygame import draw
from .consts import params, colors

class CircleSprite():
    def __init__(self, surface) -> None:
        self.surface = surface
        self.center_x = params.SCREEN_X // 2
        self.center_y = params.SCREEN_Y // 2
        self.radius = params.SIZE

    def draw(self):
        draw.circle(self.surface, colors.WHITE, (self.center_x, self.center_y), self.radius, 0)
