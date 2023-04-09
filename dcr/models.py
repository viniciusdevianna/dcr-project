from abc import ABCMeta, abstractmethod
from .consts import params

class Movable(metaclass=ABCMeta):
    @abstractmethod
    def move():
        pass

class Circle(Movable):
    def __init__(self, sprite) -> None:
        self.sprite = sprite
        self.vel = params.SPEED

    def move(self):
        self.sprite.center_x += self.vel
        if params.SCREEN_X <= self.sprite.center_x + self.sprite.radius:
            self.vel = -self.vel
        if 0 >= self.sprite.center_x - self.sprite.radius:
            self.vel = -self.vel

    def draw(self):
        self.sprite.draw()