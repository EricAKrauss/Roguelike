global IDCounter
IDCounter = 0

VERSION = "0.1.0"

WALL = '#'
SPACE= '.'
CORRIDOR = '.'
DOOR = 'D'
DECORATION='*'
PLAYER = '@'
STAIRS = ['S','E']
UNKNOWN= ' '
TREE = 'T'

ENEMY = 'x'
ENEMY_ELITE= 'X'

HEALTH= '+'
ITEM= '?'
GOLD = '$'
CHEST= '='
BRUSH= '"'
WATER= '~'
SMOKE= chr(176)
NEST = chr(235)
BOMB = 'o'

COLOR_DEFAULT = [255, 255, 255]
COLOR_BLACK = [0,0,0]
COLOR_FOW = [100, 100, 100]

COLOR_DOOR = [64, 68, 2]
COLOR_WALL = [124, 132, 7]
COLOR_BRUSH= [30, 110, 30]
COLOR_TREE = [30, 110, 30]
COLOR_SMOKE= [80, 80, 80]
COLOR_GHOST= [89, 152, 255]

COLOR_GOLD = [190, 204, 8]
COLOR_ITEM = [31, 2, 68]
COLOR_CHEST= [81, 79, 13]

COLOR_ALLY = [27, 107, 27]
COLOR_PLAYER=[31, 89, 183]
COLOR_ENEMY =[140, 7, 31]
COLOR_HAZARD=[216,105,15]
