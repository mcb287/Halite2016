import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
logging.basicConfig(filename='example.log',level=logging.INFO)
logging.info('Start log ---------------------')
myID, game_map = hlt.get_init()
hlt.send_init("Mr. Red Parakeet")

def populate_lists(game_map):
    logging.info('****populate_lists****')
    my_squares = []
    empty_squares =[]
    enemies =[]
    enemy_squares = []
    for square in game_map:
        if(square.owner == 0):
            logging.info('adding empty')
            empty_squares.append(square)
        elif(square.owner == myID):
            logging.info('adding owned')
            my_squares.append(square)
        else:
            if square.owner not in enemies:
                logging.info('adding enemy')
                enemies.append(square.owner)
                logging.info('adding enemy square')
                enemy_squares.append(square.owner)
            enemy_squares[[enemy_squares.index(square.owner)].append(square)]
    logging.error('test')

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
        return Move(square, random.choice((NORTH, WEST, SOUTH, EAST)))

while True:
    game_map.get_frame()
    populate_lists(game_map)
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
