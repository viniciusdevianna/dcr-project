from .utils.classes import Clickable, Button
from .consts.states import States
from .consts import params
from pygame import constants as pg
from pygame import mouse as mouse
import random

class BaseUI():
    def __init__(self, view, statemachine, player, opponent) -> None:
        self.view = view
        self.statemachine = statemachine
        self.player = player
        self.opponent = opponent
        self.round = 0
        self.confirm_button = Button(self.view.confirm_button_view, on_click = self._confirm_button_click)

    def initial_load(self, card_sprite):
        self.player.load_deck(card_sprite)
        self.opponent.load_deck(card_sprite)
        self.statemachine.next_battle_stage()

    def _confirm_button_click(self):
        if self.statemachine.state == States.SUMMONING:
            self.statemachine.next_battle_stage()
        if self.statemachine.state == States.IDLE:
            self.statemachine.next_battle_stage()

    def draw(self):
        self.view.draw(self.statemachine.state, self.player, self.opponent)

    def toggle_description(self, description):
        self.view.show_description = not self.view.show_description
        self.view.description = description

    def calculate_rules(self):
        if self.statemachine.state == States.DRAWING:
            self._calculate_rules_drawing()
        if self.statemachine.state == States.PREPARING_BATTLE:
            self._calculate_rules_preparing_battle()
        if self.statemachine.state == States.BATTLING:
            self._calculate_rules_battling()
        if self.statemachine.state == States.ENDING_BATTLE:
            self._calculate_rules_ending_battle()
        if self.statemachine.state == States.AFTER_BATTLE:
            self._calculate_rules_after_battle()

    def process_events(self, events):
        for e in events:
            if e.type == pg.QUIT:
                exit()
        if self.statemachine.state == States.SUMMONING:
            self._process_events_summoning(events)
        if self.statemachine.state == States.IDLE:
            self._process_events_idle(events)

    def _calculate_rules_drawing(self):
        self.player.draw_cards()
        self.opponent.draw_cards()
        for card in self.opponent.hand:
            card.selected = random.choice([True, False])
        self.statemachine.next_battle_stage()

    def _calculate_rules_preparing_battle(self):
        self.player.calculate_battle_stats()
        self.opponent.calculate_battle_stats()
        self.statemachine.next_battle_stage()

    def _calculate_rules_battling(self):
        player_previous_health = self.player.total_health
        opponent_previous_health = self.opponent.total_health
        
        if self.opponent.total_health > 0 and self.player.total_power > 0:
            self.opponent.total_health -= 1
            self.player.total_power -= 1
        if self.player.total_health > 0 and self.opponent.total_power > 0:
            self.player.total_health -= 1
            self.opponent.total_power -= 1
        
        if player_previous_health == self.player.total_health and opponent_previous_health == self.opponent.total_health:
            self.statemachine.next_battle_stage()

    def _calculate_rules_ending_battle(self):
        if self.player.total_health > self.opponent.total_health:
            self.player.won_round()
        elif self.player.total_health < self.opponent.total_health:
            self.opponent.won_round()
        else:
            self.player.won_round()
            self.opponent.won_round()

        print(self.player.score)
        self.round += 1
        self.statemachine.next_battle_stage()

    def _calculate_rules_after_battle(self):
        self.player.move_all_cards(self.player.hand, self.player.trash)
        self.player.move_all_cards(self.player.summoned, self.player.trash)
        self.opponent.move_all_cards(self.opponent.hand, self.opponent.trash)
        self.opponent.move_all_cards(self.opponent.summoned, self.opponent.trash)
        if self.round > params.ROUNDS:
            if self.player.score < params.ROUNDS_TO_WIN:
                self.statemachine.declare_loss()
            elif self.opponent.score < params.ROUNDS_TO_WIN:
                self.statemachine.declare_win()
            else:
                self.statemachine.declare_draw()
        elif self.player.score == params.ROUNDS_TO_WIN:
            self.statemachine.declare_win()
        elif self.opponent.score == params.ROUNDS_TO_WIN:
            self.statemachine.declare_loss()
        else:
            self.statemachine.next_battle_stage()
        
    def _process_events_summoning(self, events):
        for e in events:
            for card in self.player.hand:
                card.process_events(e, self)
            self.confirm_button.process_events(e)

    def _process_events_idle(self, events):
        for e in events:
            self.confirm_button.process_events(e)


class Card(Clickable):
    def __init__(self, name, color, sprite, description):
        self.name = name
        self.color = color
        self.sprite = sprite
        self.description = description
        self.selected = False
        self.frame = None

    def _onRightClick(self, event, base_ui):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_RIGHT:
                position = mouse.get_pos()
                if self.frame.collidepoint(position):
                    self._show_description(base_ui)

    def _onLeftClick(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                position = mouse.get_pos()
                if self.frame.collidepoint(position):
                    self.selected = not self.selected

    def _show_description(self, base_ui):
        base_ui.toggle_description(self.description)

    def draw(self, left, top):
        self.sprite.draw(left, top, self.selected)
        self.frame = self.sprite.frame

    def process_events(self, event, base_ui):
        self._onRightClick(event, base_ui)
        self._onLeftClick(event)

class DigimonCard(Card):
    def __init__(self, name, color, sprite, description, power=0, health=0):
        self.power = power
        self.health = health
        super().__init__(name, color, sprite, description)

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
    
    def remove(self, card):
        self.cards.remove(card)
        self.size = len(self.cards)
    
    def append(self, card):
        self.cards.append(card)
        self.size = len(self.cards)
    
class Player():
    def __init__(self, name) -> None:
        self.name = name
        self.deck = None
        self.hand = []
        self.trash = []
        self.summoned = []
        self.total_power = 0
        self.total_health = 0
        self.score = 0
    
    def load_deck(self, card_sprite):
        cards = []
        for _ in range(40):
            card = DigimonCard('Card', 'Brown', card_sprite, 'This is a test card', random.randrange(0, 21), random.randrange(0, 21))
            cards.append(card)
        self.deck = Deck(cards)

    def draw_cards(self):
        for _ in range(params.HAND_SIZE):
            self.hand.append(self.deck.draw_card())

    def move_card(self, from_where, move_to, card):
        move_to.append(card)
        from_where.remove(card)

    def move_all_cards(self, from_where, move_to):
        cards = [card for card in from_where]
        for card in cards:
            self.move_card(from_where, move_to, card)

    def calculate_battle_stats(self):
        for card in self.hand:
            if card.selected:
                card.selected = False
                self.summoned.append(card)

        new_hand = [card for card in self.hand if card not in self.summoned]
        self.hand = new_hand

        self.total_power = sum(card.power for card in self.summoned)
        self.total_health = sum(card.health for card in self.summoned)

    def won_round(self):
        self.score += 1
    
    