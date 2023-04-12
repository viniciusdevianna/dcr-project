import os
from pathlib import Path

# Sizes
SCREEN_X = 800
SCREEN_Y = 600
SIZE = SCREEN_Y // 10

# Movement
SPEED = 1

# Battling players
PLAYER = 'P'
OPPONENT = 'O'
DRAW = 'D'

# Game mechanics
HAND_SIZE = 6
ROUNDS = 5
ROUNDS_TO_WIN = 3

# Folders
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
BASE_IMG_DIR = os.path.join(BASE_ASSETS_DIR, 'img')
CARDS_IMG_DIR = os.path.join(BASE_IMG_DIR, 'cards')
