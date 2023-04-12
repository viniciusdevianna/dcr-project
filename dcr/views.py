from pygame import draw, image, Surface
from .consts import params, colors, states
from .utils.functions import draw_text_on_surface

class BaseUIView():
    def __init__(self, surface, font) -> None:
        self.surface = surface
        self.font = font
        self.show_description = False
        self.description = None
        self.confirm_button_view = ButtonSprite(self.surface, self.font, params.SCREEN_X - 70, params.SCREEN_Y - 100)

    def draw(self, state, player, opponent):
        if state == states.States.SUMMONING:
            self._draw_summoning(player)        
        if state == states.States.BATTLING or state == states.States.ENDING_BATTLE or state == states.States.IDLE:
            self._draw_battling(player, opponent)
        if state == states.States.WINNING or state == states.States.LOSING:
            self._draw_ending_message(state)

    def _draw_description(self):
        height = 50
        width = params.SCREEN_X
        draw.rect(self.surface, colors.WHITE_TRANSPARENT, (0, params.SCREEN_Y - height, width, height), 0)

        text = self.description if self.description is not None else ''
        description_x = 5
        description_y = params.SCREEN_Y - height + 5
        draw_text_on_surface(self.surface, self.font, colors.BLACK, text, description_x, description_y)

    def _draw_cards(self, cards, card_x, card_y):
        for card in cards:
            card.draw(card_x, card_y)
            card_x += card.sprite.width + 4

    def _draw_summoning(self, player):
        self._draw_cards(player.hand, 2, 2)
        self.confirm_button_view.draw()

        self._draw_deck_counter(player)
        self._draw_trash_counter(player)
        
        if self.show_description:
            self._draw_description()

    def _draw_battling(self, player, opponent):
        self._draw_cards(player.summoned, 2, params.SCREEN_Y - 150 - 4)
        self._draw_cards(opponent.summoned, 2, 2)
        self.confirm_button_view.draw()

        self._draw_deck_counter(player)
        self._draw_trash_counter(player)
        self._draw_deck_counter(opponent, False)
        self._draw_trash_counter(opponent, False)

        stats_player = f'{player.total_power} / {player.total_health}'
        player_stats_x = params.SCREEN_X - 70
        player_stats_y = params.SCREEN_Y - 30
        draw_text_on_surface(self.surface, self.font, colors.WHITE, stats_player, player_stats_x, player_stats_y)

        stats_opponent = f'{opponent.total_power} / {opponent.total_health}'
        opponent_stats_x = params.SCREEN_X - 70
        opponent_stats_y = 30
        draw_text_on_surface(self.surface, self.font, colors.WHITE, stats_opponent, opponent_stats_x, opponent_stats_y)

    def _draw_ending_message(self, state):
        if state == states.States.WINNING:
            msg = 'Você venceu!'
        elif state == states.States.LOSING:
            msg = 'Você perdeu...'
        else:
            msg = 'Foi um empate!'
        msg_x = params.SCREEN_X // 2
        msg_y = params.SCREEN_Y // 2
        draw_text_on_surface(self.surface, self.font, colors.PRIMARY, msg, msg_x, msg_y)

    def _draw_deck_counter(self, owner, is_player=True):
        text = f'Deck: {owner.deck.size}'
        text_x = params.SCREEN_X - 70
        text_y = params.SCREEN_Y // 2 + 30 if is_player else params.SCREEN_Y // 2 - 30
        draw_text_on_surface(self.surface, self.font, colors.WHITE, text, text_x, text_y)

    def _draw_trash_counter(self, owner, is_player=True):
        text = f'Trash: {len(owner.trash)}'
        text_x = params.SCREEN_X - 120
        text_y = params.SCREEN_Y // 2 + 30 if is_player else params.SCREEN_Y // 2 - 30
        draw_text_on_surface(self.surface, self.font, colors.WHITE, text, text_x, text_y)

class CardSprite():
    def __init__(self, surface, font, image='no-image.jpg') -> None:
        self.surface = surface
        self.font = font
        self.image = f'{params.CARDS_IMG_DIR}\\{image}'
        self.width = 100
        self.height = 150
        self.frame = None

    def draw(self, left, top, suit, selected, power=None, health=None):
        # Draw card frame
        frame = draw.rect(self.surface, suit, (left, top, self.width, self.height), 0)

        # Draw card img
        img = image.load(self.image)
        self.surface.blit(img, (left + 2, top + 2))

        # Draw card power and health if digimon card
        if power is not None and health is not None:
            ph_text = f'{power} / {health}'
            ph_img = self.font.render(ph_text, True, colors.BLACK)
            temp_surface = Surface(ph_img.get_size())
            temp_surface.fill(colors.WHITE_TRANSPARENT)
            ph_x = left + self.width - ph_img.get_width() - 5
            ph_y = top + self.height - ph_img.get_height() - 5
            temp_surface.blit(ph_img, (0, 0))
            self.surface.blit(temp_surface, (ph_x, ph_y))

        if selected:
            draw.rect(self.surface, colors.SELECTED, (left, top, self.width, self.height), 2)

        self.frame = frame
    
class ButtonSprite():
    def __init__(self, surface, font, left, top, width=60, height=30, color=colors.PRIMARY, text='Confirmar') -> None:
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
        btn_text_x = self.left + 5
        btn_text_y = self.top + 5
        draw_text_on_surface(self.surface, self.font, colors.WHITE, self.text, btn_text_x, btn_text_y)

        self.frame = frame
