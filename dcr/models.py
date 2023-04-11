from abc import ABCMeta, abstractmethod
from .consts import params
from pygame import constants as pg
from pygame import mouse as mouse

class Clickable(metaclass=ABCMeta):
    @abstractmethod
    def _onRightClick(self, event):
        pass

    @abstractmethod
    def _onLeftClick(self, event):
        pass

class BaseUI():
    def __init__(self, view) -> None:
        self.view = view

    def draw(self):
        self.view.draw()

    def toggle_description(self, description):
        self.view.show_description = not self.view.show_description
        self.view.description = description

class Card(Clickable):
    def __init__(self, base_UI, name, color, sprite, description):
        self.base_UI = base_UI
        self.name = name
        self.color = color
        self.sprite = sprite
        self.description = description
        self.selected = False
        self.frame = None

    def _onRightClick(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_RIGHT:
                position = mouse.get_pos()
                if self.frame.collidepoint(position):
                    self.base_UI.toggle_description(self.description)

    def _onLeftClick(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                position = mouse.get_pos()
                if self.frame.collidepoint(position):
                    self.selected = not self.selected

    def draw(self, left, top):
        self.frame = self.sprite.draw(left, top, self.selected)

    def process_events(self, event):
        self._onRightClick(event)
        self._onLeftClick(event)

class DigimonCard(Card):
    def __init__(self, base_UI, name, color, sprite, description, power=0, health=0):
        self.power = power
        self.health = health
        super().__init__(base_UI, name, color, sprite, description)

    def draw(self, left, top):
        self.frame = self.sprite.draw(left, top, self.selected, self.power, self.health)
        

    