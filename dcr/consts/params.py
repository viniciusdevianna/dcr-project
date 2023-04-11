import os
from pathlib import Path

# Sizes
SCREEN_X = 800
SCREEN_Y = 600
SIZE = SCREEN_Y // 10

# Movement
SPEED = 1

# Folders
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
BASE_IMG_DIR = os.path.join(BASE_ASSETS_DIR, 'img')
CARDS_IMG_DIR = os.path.join(BASE_IMG_DIR, 'cards')
