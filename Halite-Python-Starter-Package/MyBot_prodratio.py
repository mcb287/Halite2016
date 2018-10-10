import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
logging.basicConfig(filename='example.log',level=logging.ERROR)
logging.info('Start log ---------------------')
myID, game_map = hlt.get_init()
hlt.send_init("Mr. Prodratio")
logging.error('1')

def get_prod_ratio(square):
    tmp_ratio = 1000
    tmp_idx = -1
    tmp_strength = 0
    for idx, n in enumerate(game_map.neighbors(square)):
        if(n.production > 0):
            if (n.strength/n.production < tmp_ratio and n.owner != myID):
                tmp_ratio = n.strength/n.production
                tmp_idx = idx
                tmp_strength = n.strength
    return tmp_idx, tmp_strength

def assign_move(square):
    n_str = ""
    wait = False
    dir_, str_ = get_prod_ratio(square)
    if(dir_ != -1 and square.strength > str_):
        return Move(square, dir_)
    elif(dir_ != -1 and square.strength < str_):
        wait = True
    if(wait or square.strength < 20):
        return Move(square, STILL)
    else:
        return Move(square, random.choice((NORTH, WEST, SOUTH, EAST)))

while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
