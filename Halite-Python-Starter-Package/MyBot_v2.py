import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
logging.basicConfig(filename='example.log',level=logging.INFO)
logging.info('Start log ---------------------')
myID, game_map = hlt.get_init()
hlt.send_init("Attack best prodratio")

def populate_lists(game_map):
    logging.info('****populate_lists****')
    my_squares = []
    empty_squares =[]
    enemies =[]
    enemy_size = []
    enemy_squares = []
    for square in game_map:
        if(square.owner == 0):
            #logging.info('adding empty')
            empty_squares.append(square)
        elif(square.owner == myID):
            #logging.info('adding owned')
            my_squares.append(square)
        else:
            if square.owner not in enemies:
                #logging.info('adding enemy')
                enemies.append(square.owner)
                enemy_squares.append([])
            #logging.info('adding enemy square')
            enemy_squares[enemies.index(square.owner)].append(square)
    #logging.info("MySquares " + str(len(my_squares)))
    #logging.info("EmptySquares " + str(len(empty_squares)))
    for e in enemies:
        #logging.info("EnemySquares enemy: " +str(e) + " " + str(len(enemy_squares[enemies.index(e)])))
        enemy_size.append(len(enemy_squares[enemies.index(e)]))
    #logging.info("Smallest enemy: " + str(enemies[enemy_size.index(min(enemy_size))]) + " | " + str(min(enemy_size))) 
    #logging.info("----------------------------")
    return my_squares, empty_squares, enemies, enemy_size, enemy_squares
    
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

def kill_smallest_enemy(square, enemies, enemy_size, enemy_squares):
    tmp_distance = game_map.width + game_map.height
    smallest_enemy = enemies[enemy_size.index(min(enemy_size))]
    enemy_index = enemies.index(smallest_enemy)
    #logging.info("smallest enemy index: " + str(enemies.index(smallest_enemy)))
    #logging.info("smallest enemy var: " + str(smallest_enemy))
    #logging.info("enemies count: " + str(len(enemies)))
    for e in enemy_squares[enemy_index]:
        #logging.info(e)
        dist = game_map.get_distance(square, e)
        if(dist < tmp_distance):
            tmp_distance = dist
            enemy_square = e
    return enemy_square

def assign_move(square):
    wait = False
    i, s = get_prod_ratio(square)
    logging.info("i: " + str(i))
    logging.info("s: " + str(s))
    if(i != -1 and s < square.strength):
        return Move(square, i)
    elif(i != -1 ):
        wait = True
        
##    for idx, n in enumerate(game_map.neighbors(square)):
##        if(n.owner != myID and n.strength < square.strength):
##           return Move(square, idx)
##        elif(n.owner != myID):
##            wait = True
    if(wait or square.strength < 35):
        return Move(square, STILL)
    else:
        return Move(square, get_direction(square, kill_smallest_enemy(square, enemies, enemy_size, enemy_squares)))
        #return Move(square, random.choice((NORTH, WEST, SOUTH, EAST)))

while True:
    game_map.get_frame()
    my_squares, empty_squares, enemies, enemy_size, enemy_squares = populate_lists(game_map)
    moves = [assign_move(square) for square in my_squares]
    hlt.send_frame(moves)
