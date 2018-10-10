import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
logging.basicConfig(filename='example.log',level=logging.ERROR)
logging.info('Start log ---------------------')
myID, game_map = hlt.get_init()
hlt.send_init("Mr. Red Parakeet")

def get_direction(square_1, square_2):
    x = square_1.x - square_2.x
    y = square_1.y - square_2.y
    logging.info('****get_direction****')
    logging.info(square_1)
    logging.info(square_2)
    if(abs(x) > abs(y)):
        if((x < 0 and abs(x) < game_map.width/2) or (x > 0 and abs(x) > game_map.width/2)):
            logging.info('Return EAST')
            logging.info('********')
            return EAST
        else:
            logging.info('Return WEST')
            logging.info('********')
            return WEST
    else:
        if((y < 0 and abs(y) < game_map.height/2) or (y > 0 and abs(y) > game_map.height/2)):
            logging.info('Return SOUTH')
            logging.info('********')
            return SOUTH
        else:
            logging.info('Return NORTH')
            logging.info('********')
            return NORTH 
        
def find_weakest_friend(square):
    tmp_s = 255
    tmp_dir = 5
    for idx, n in enumerate(game_map.neighbors(square)):
        if(n.strength < tmp_s):
            tmp_s = n.strength
            tmp_dir = idx
    return tmp_dir

def find_closest_non_friend(square):
    first = True
    tmp_dist = 0 
    ret_square = square 
    for square_2 in game_map:
        if((game_map.get_distance(square, square_2) < tmp_dist or first) and square_2.owner != myID):
            first = False
            tmp_dist = game_map.get_distance(square, square_2)
            ret_square = square_2
    return ret_square
         
def assign_move(square):
    n_str = ""
    wait = False
    for idx, n in enumerate(game_map.neighbors(square)):
        if(n.owner != myID and n.strength < square.strength):
           return Move(square, idx)
        elif(n.owner != myID):
            wait = True
    if(wait or square.strength < 10):
        return Move(square, STILL)
    else:
        return Move(square, get_direction(square, find_closest_non_friend(square)))
#    elif(square.strength > 200):
#        return Move(square, get_direction(square, find_closest_non_friend(square)))
#    else:
#        return Move(square, find_weakest_friend(square))


while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
