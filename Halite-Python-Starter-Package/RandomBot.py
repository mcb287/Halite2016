import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random


myID, game_map = hlt.get_init()
hlt.send_init("RandomPythonBot")
def random_move(square):
    if (square.strength > 25):
        return random.choice((NORTH, EAST, SOUTH, WEST, STILL))
    else:
        return STILL
while True:
    game_map.get_frame()
    moves = [Move(square, random_move(square)) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
