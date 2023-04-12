from abc import ABCMeta, abstractmethod
from . import views
from .consts import colors
from pygame import constants as pg
from pygame import mouse as mouse

class Clickable(metaclass=ABCMeta):
    @abstractmethod
    def _onRightClick(self, event):
        pass

    @abstractmethod
    def _onLeftClick(self, event):
        pass

class Button(Clickable):
    def __init__(self, sprite, on_click=lambda _: {}):
        self.sprite = sprite
        self.on_click = on_click

    def _onRightClick(self, event):
        pass

    def _onLeftClick(self, event):
        self.on_click()

    def process_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                position = mouse.get_pos()
                if self.sprite.frame.collidepoint(position):
                    self._onLeftClick(event)