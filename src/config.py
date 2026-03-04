# config.py
import random

GRID_ROWS = random.randint(8, 10)
GRID_COLS = random.randint(8, 10)

START = (0, 0)
GOAL = (GRID_ROWS - 1, GRID_COLS - 1)

MAX_LIVES = 4

WALK_TIME = 2
JUMP_TIME = 3
TURN_COST = 1

LAND = "L"
VOLCANO = "V"
WATER = "W"
BRICK = "B"

HAZARDS = [VOLCANO, WATER]