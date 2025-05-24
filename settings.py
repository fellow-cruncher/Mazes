from sets import SETS

FPS = 80
BACKGROUND_COLOR = "gray20"
UNKNOWN = "??"

# MUST BE ODD
ROWS = 59
COLS = 41

# BORDERS AND LINES
BRDR_POS = ((23,31),  (656,31),  (1289,31),
            (23,747), (656,747), (1289,747))
BRDR_SIZE = (610,430)
BRDR_COLOR = LINE_COLOR = "gray10"

LINES_STARTS = ((0, 602), (451, 602), (1062, 602), (1713, 602))
LINES_ENDS = ((187, 602), (862, 602), (1473, 602), (1920, 602))

# BOARDS
BRD_POS = ((33,41),  (666,41),  (1299,41),
           (33,757), (666,757), (1299,757))
BRD_COLOR = "gray50"
START_COLOR = "magenta"
STOP_COLOR = "red3"

# STATS
X = [240,530,865,1155,1510,1800]
Y = [495,555,650,710]

# DO NOT CHANGE
CRIT_POS = [
    [(X[0],Y[0]),(X[1],Y[0]),
     (X[0],Y[1]),(X[1],Y[1])],
     
    [(X[2],Y[0]),(X[3],Y[0]),
     (X[2],Y[1]),(X[3],Y[1])],
      
    [(X[4],Y[0]),(X[5],Y[0]),
     (X[4],Y[1]),(X[5],Y[1])],

    [(X[0],Y[2]),(X[1],Y[2]),
     (X[0],Y[3]),(X[1],Y[3])],
     
    [(X[2],Y[2]),(X[3],Y[2]),
     (X[2],Y[3]),(X[3],Y[3])],
     
    [(X[4],Y[2]),(X[5],Y[2]),
     (X[4],Y[3]),(X[5],Y[3])]
]

PATH_COLOR = "yellow2"
PATH_RUN_COLOR = "gold3"
CLOSED_COLOR = "seagreen2"
EDGE_COLOR = "seagreen4"
PLACE_COLOR = "steelblue3"
NUM_COLOR = "gray90"

# LEVELS
LEV_COLOR = "gold3"
LEVEL_POS = [
    (625,475),(1258,475),(1891,475),
    (625,725),(1258,725),(1891,725)
]