from .utils import Clickable, Button
from .consts.states import States
from pygame import constants as pg
from pygame import mouse as mouse
import random

class BaseUI():
    def __init__(self, view, statemachine, player, opponent) -> None:
        self.view = view
        self.statemachine = statemachine
        self.player = player
        self.opponent = opponent
        self.confirm_button = Button(self.view.confirm_button_view, on_click = self._confirm_button_click)

    def initial_load(self, card_sprite):
        self.player.load_deck(card_sprite)
        self.opponent.load_deck(card_sprite)

    def _confirm_button_click(self):
        self.statemachine.battle_phase()

    def draw(self):
        self.view.draw(self.statemachine.state, self.player, self.opponent)

    def toggle_description(self, description):
        self.view.show_description = not self.view.show_description
        self.view.description = description

    def calculate_rules(self):
        if self.statemachine.state == States.DRAWING:
            self._calculate_rules_drawing()
        if self.statemachine.state == States.BATTLING:
            self._calculate_rules_battling()

    def process_events(self, events):
        for e in events:
            if e.type == pg.QUIT:
                exit()
        if self.statemachine.state == States.SUMMONING:
            self._process_events_summoning(events)

    def _calculate_rules_drawing(self):
        self.player.draw_cards()
        self.opponent.draw_cards()
        for card in self.opponent.hand:
            card.selected = random.choice([True, False])
        self.statemachine.summon_phase()

    def _calculate_rules_battling(self):
        self.player.calculate_battle_stats()
        self.opponent.calculate_battle_stats()

    def _process_events_summoning(self, events):
        for e in events:
            for card in self.player.hand:
                card.process_events(e)
            self.confirm_button.process_events(e)


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
        self.sprite.draw(left, top, self.selected)
        self.frame = self.sprite.frame

    def process_events(self, event):
        self._onRightClick(event)
        self._onLeftClick(event)

class DigimonCard(Card):
    def __init__(self, base_UI, name, color, sprite, description, power=0, health=0):
        self.power = power
        self.health = health
        super().__init__(base_UI, name, color, sprite, description)

    def draw(self, left, top):
        self.sprite.draw(left, top, self.selected, self.power, self.health)
        self.frame = self.sprite.frame

class Deck():
    def __init__(self, cards) -> None:
        self.cards = cards
        self.size = len(cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        card = self.cards.pop(0)
        self.size = len(self.cards)
        return card
    
class Player():
    def __init__(self, name) -> None:
        self.name = name
        self.deck = None
        self.hand = []
        self.total_power = 0
        self.total_health = 0
    
    def load_deck(self, card_sprite):
        cards = []
        for _ in range(40):
            card = DigimonCard(self, 'Card', 'Brown', card_sprite, 'This is a test card', random.randrange(0, 21), random.randrange(0, 21))
            cards.append(card)
        self.deck = Deck(cards)

    def draw_cards(self):
        for _ in range(6):
            self.hand.append(self.deck.draw_card())

    def calculate_battle_stats(self):
        self.total_power = sum(card.power for card in self.hand if card.selected)
        self.total_health = sum(card.health for card in self.hand if card.selected)
    
    