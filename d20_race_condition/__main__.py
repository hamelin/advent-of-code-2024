from tqdm.auto import tqdm
from . import *  # noqa


INPUT = """\
#############################################################################################################################################
#...#...#.................#...#.....#.....#...###...###...#.........#...###...........#.....#...#######...#.....#.............#.......###...#
#.#.#.#.#.###############.#.#.#.###.#.###.#.#.###.#.###.#.#.#######.#.#.###.#########.#.###.#.#.#######.#.#.###.#.###########.#.#####.###.#.#
#.#.#.#.#...#.........#...#.#.#.#...#.#...#.#.#...#.#...#.#.....#...#.#.....#.........#.#...#.#...###...#.#...#.#.....#.....#...#.....#...#.#
#.#.#.#.###.#.#######.#.###.#.#.#.###.#.###.#.#.###.#.###.#####.#.###.#######.#########.#.###.###.###.###.###.#.#####.#.###.#####.#####.###.#
#.#...#...#.#.#.....#.#.###.#...#.#...#.#...#.#...#.#...#.#.....#...#.......#.#...#.....#...#...#...#.#...#...#.#...#.#...#.#.....#.....#...#
#.#######.#.#.#.###.#.#.###.#####.#.###.#.###.###.#.###.#.#.#######.#######.#.#.#.#.#######.###.###.#.#.###.###.#.#.#.###.#.#.#####.#####.###
#.#.......#...#...#...#.#...#.....#...#.#.#...#...#...#.#.#.......#...#...#.#.#.#.#.#.......###...#.#.#.###.#...#.#...#...#...#...#.....#...#
#.#.#############.#####.#.###.#######.#.#.#.###.#####.#.#.#######.###.#.#.#.#.#.#.#.#.###########.#.#.#.###.#.###.#####.#######.#.#####.###.#
#.#.#...#...#...#.....#...#...###...#.#.#.#...#...#...#.#.#...###...#...#...#...#...#...###...#...#...#.....#...#...#...###...#.#.#...#.#...#
#.#.#.#.#.#.#.#.#####.#####.#####.#.#.#.#.###.###.#.###.#.#.#.#####.###################.###.#.#.###############.###.#.#####.#.#.#.#.#.#.#.###
#.#.#.#.#.#...#.....#.....#.#...#.#.#.#.#...#.....#.....#...#.#.....#.........#...#.....#...#.#.#.........#.....#...#.#...#.#.#.#...#...#...#
#.#.#.#.#.#########.#####.#.#.#.#.#.#.#.###.#################.#.#####.#######.#.#.#.#####.###.#.#.#######.#.#####.###.#.#.#.#.#.###########.#
#.#.#.#.#.......#...#.....#.#.#.#.#.#.#.###.......#.........#.#...#...#...###...#...#...#...#.#.#.......#...#...#.#...#.#.#.#...#.........#.#
#.#.#.#.#######.#.###.#####.#.#.#.#.#.#.#########.#.#######.#.###.#.###.#.###########.#.###.#.#.#######.#####.#.#.#.###.#.#.#####.#######.#.#
#.#...#.###...#.#...#.....#...#.#.#...#...#...###...#...###.#.###.#...#.#...#.........#.#...#...#...#...#...#.#.#.#.#...#...#.....#...###...#
#.#####.###.#.#.###.#####.#####.#.#######.#.#.#######.#.###.#.###.###.#.###.#.#########.#.#######.#.#.###.#.#.#.#.#.#.#######.#####.#.#######
#.#...#.....#...#...#.....#.....#.....#...#.#.#.....#.#.#...#...#.#...#.#...#.#.........#.......#.#...#...#.#.#.#.#.#.#.......#.....#.#...###
#.#.#.###########.###.#####.#########.#.###.#.#.###.#.#.#.#####.#.#.###.#.###.#.###############.#.#####.###.#.#.#.#.#.#.#######.#####.#.#.###
#.#.#.#...#.....#.###.....#.#...#.....#...#.#.#...#.#.#.#.#...#...#...#.#...#.#...#...#.....#...#...###.#...#.#.#.#.#.#...#...#.#.....#.#...#
#.#.#.#.#.#.###.#.#######.#.#.#.#.#######.#.#.###.#.#.#.#.#.#.#######.#.###.#.###.#.#.#.###.#.#####.###.#.###.#.#.#.#.###.#.#.#.#.#####.###.#
#...#...#.#.#...#...#...#.#.#.#.#.......#.#.#...#.#...#.#...#...#.....#...#...#...#.#.#...#...#.....#...#...#.#...#...#...#.#.#.#.#...#...#.#
#########.#.#.#####.#.#.#.#.#.#.#######.#.#.###.#.#####.#######.#.#######.#####.###.#.###.#####.#####.#####.#.#########.###.#.#.#.#.#.###.#.#
#.........#.#.....#...#...#.#.#...#...#.#.#...#.#.....#.......#.#...#.....#.....#...#...#.....#.#...#.#.....#.#...#.....#...#...#...#.....#.#
#.#########.#####.#########.#.###.#.#.#.#.###.#.#####.#######.#.###.#.#####.#####.#####.#####.#.#.#.#.#.#####.#.#.#.#####.#################.#
#...#.......#...#.#.......#...#...#.#.#.#.#...#.#...#.......#.#.#...#...#...#...#.....#.#...#.#.#.#...#.#...#.#.#.#.....#...#...........#...#
###.#.#######.#.#.#.#####.#####.###.#.#.#.#.###.#.#.#######.#.#.#.#####.#.###.#.#####.#.#.#.#.#.#.#####.#.#.#.#.#.#####.###.#.#########.#.###
#...#.#.......#.#...#...#.....#...#.#.#.#.#...#...#.#...#...#...#.#...#.#.###.#.#.....#.#.#...#.#.#.....#.#.#.#.#...#...#...#.........#.#.###
#.###.#.#######.#####.#.#####.###.#.#.#.#.###.#####.#.#.#.#######.#.#.#.#.###.#.#.#####.#.#####.#.#.#####.#.#.#.###.#.###.###########.#.#.###
#.....#.......#.....#.#.#...#...#...#...#...#.#...#...#.#...#.....#.#.#.#.#...#.#.....#.#.#.....#.#.###...#...#...#...###.#...#.......#.#...#
#############.#####.#.#.#.#.###.###########.#.#.#.#####.###.#.#####.#.#.#.#.###.#####.#.#.#.#####.#.###.#########.#######.#.#.#.#######.###.#
#...#...#...#.....#.#.#...#.....#.......#...#...#...#...#...#.#...#.#.#.#.#.#...#...#.#...#...#...#...#...#.......#...#...#.#...###...#.....#
#.#.#.#.#.#.#####.#.#.###########.#####.#.#########.#.###.###.#.#.#.#.#.#.#.#.###.#.#.#######.#.#####.###.#.#######.#.#.###.#######.#.#######
#.#...#...#.....#.#.#.............#...#.#.#...#...#.#.###...#.#.#.#.#.#.#.#.#.###.#.#.....#...#...#...#...#.......#.#.#.#...###...#.#.......#
#.#############.#.#.###############.#.#.#.#.#.#.#.#.#.#####.#.#.#.#.#.#.#.#.#.###.#.#####.#.#####.#.###.#########.#.#.#.#.#####.#.#.#######.#
#.............#...#.#...#...#...#...#...#.#.#.#.#.#.#.....#.#.#.#.#.#.#.#...#...#.#.#...#.#...#...#.#...#.......#.#.#...#.......#...#.......#
#############.#####.#.#.#.#.#.#.#.#######.#.#.#.#.#.#####.#.#.#.#.#.#.#.#######.#.#.#.#.#.###.#.###.#.###.#####.#.#.#################.#######
#.......#...#.....#...#...#...#.#.......#.#.#.#.#.#...#...#.#.#.#.#.#.#.....###.#.#.#.#.#...#.#...#...###.....#...#...#.........#...#...#...#
#.#####.#.#.#####.#############.#######.#.#.#.#.#.###.#.###.#.#.#.#.#.#####.###.#.#.#.#.###.#.###.###########.#######.#.#######.#.#.###.#.#.#
#.....#.#.#.......#.....#.....#.#.......#.#.#.#.#...#.#.#...#.#.#.#.#.#...#...#.#.#.#.#.#...#...#.#.........#.#...###.#.......#.#.#.....#.#.#
#####.#.#.#########.###.#.###.#.#.#######.#.#.#.###.#.#.#.###.#.#.#.#.#.#.###.#.#.#.#.#.#.#####.#.#.#######.#.#.#.###.#######.#.#.#######.#.#
#...#.#.#...........#...#.#...#.#.......#.#.#.#.#...#.#...###.#.#...#.#.#.#...#.#.#.#.#.#.....#...#.......#.#...#.....#.......#...###.....#.#
#.#.#.#.#############.###.#.###.#######.#.#.#.#.#.###.#######.#.#####.#.#.#.###.#.#.#.#.#####.###########.#.###########.#############.#####.#
#.#...#...........###...#.#...#.........#.#.#...#...#.#.......#.....#.#.#.#.#...#.#.#.#.....#...#.........#...........#.....#...#...#.#.....#
#.###############.#####.#.###.###########.#.#######.#.#.###########.#.#.#.#.#.###.#.#.#####.###.#.###################.#####.#.#.#.#.#.#.#####
#.#...#.........#.#...#...###...........#.#...#...#.#.#.#.....#.....#...#.#.#.#...#.#.#.....#...#.#.......#.........#.#...#...#...#...#.....#
#.#.#.#.#######.#.#.#.#################.#.###.#.#.#.#.#.#.###.#.#########.#.#.#.###.#.#.#####.###.#.#####.#.#######.#.#.#.#################.#
#...#...#...#...#...#...###...#.........#.....#.#...#.#.#.#...#.........#...#.#...#.#.#.#...#...#.#.#.....#.#.......#...#.#...#...#.........#
#########.#.#.#########.###.#.#.###############.#####.#.#.#.###########.#####.###.#.#.#.#.#.###.#.#.#.#####.#.###########.#.#.#.#.#.#########
###.......#...#...#...#.....#.#...........###...#...#.#.#.#.#.....#...#...###.....#.#.#.#.#.....#...#.#...#.#...........#.#.#.#.#.#.........#
###.###########.#.#.#.#######.###########.###.###.#.#.#.#.#.#.###.#.#.###.#########.#.#.#.###########.#.#.#.###########.#.#.#.#.#.#########.#
#...#...........#...#...#...#.....#.....#...#.....#.#.#.#.#.#.###.#.#.#...#...#...#...#.#...#...#...#...#...#...........#.#.#.#.#.....#.....#
#.###.#################.#.#.#####.#.###.###.#######.#.#.#.#.#.###.#.#.#.###.#.#.#.#####.###.#.#.#.#.#########.###########.#.#.#.#####.#.#####
#.....#...............#...#.#...#...#...#...#...###.#.#.#.#.#.#...#.#.#.....#...#.###...#...#.#...#...###...#...........#...#...###...#.....#
#######.#############.#####.#.#.#####.###.###.#.###.#.#.#.#.#.#.###.#.###########.###.###.###.#######.###.#.###########.###########.#######.#
#.....#.......#.....#.#...#.#.#.#...#...#.#...#...#...#...#...#...#.#...#.....#...#...#...###.......#.#...#...........#...###.......#...#...#
#.###.#######.#.###.#.#.#.#.#.#.#.#.###.#.#.#####.###############.#.###.#.###.#.###.###.###########.#.#.#############.###.###.#######.#.#.###
#.#...###...#...#...#.#.#.#.#.#...#...#...#.#.....###.....###.....#.#...#...#...###...#...#...#...#.#.#.............#...#...#...#...#.#.#...#
#.#.#####.#.#####.###.#.#.#.#.#######.#####.#.#######.###.###.#####.#.#####.#########.###.#.#.#.#.#.#.#############.###.###.###.#.#.#.#.###.#
#.#...#...#...###...#.#.#.#...#.......#...#.#.###...#.#...#...#...#.#.#...#.........#.#...#.#...#...#...............###.....###...#.#.#.#...#
#.###.#.#####.#####.#.#.#.#####.#######.#.#.#.###.#.#.#.###.###.#.#.#.#.#.#########.#.#.###.#######################################.#.#.#.###
#...#.#.....#...#...#...#.......#.......#...#.....#...#...#...#.#...#.#.#.#...#...#.#.#.#...#...#.............................###...#.#.#...#
###.#.#####.###.#.###############.#######################.###.#.#####.#.#.#.#.#.#.#.#.#.#.###.#.#.###########################.###.###.#.###.#
###.#.###...#...#.....#...#.......#...............#...#...#...#.#.....#.#...#...#.#.#.#.#.#...#.#.#.............#...#...#...#...#.....#...#.#
###.#.###.###.#######.#.#.#.#######.#############.#.#.#.###.###.#.#####.#########.#.#.#.#.#.###.#.#.###########.#.#.#.#.#.#.###.#########.#.#
#...#.....#...#...#...#.#.#.#.....#.............#...#...###.#...#.....#.....#.....#.#...#...###...#...........#.#.#...#.#.#.....###.....#...#
#.#########.###.#.#.###.#.#.#.###.#############.###########.#.#######.#####.#.#####.#########################.#.#.#####.#.#########.###.#####
#.#...#...#.#...#...#...#.#.#...#.....#...#...#...........#.#.#.......#.....#.......#...#...###...###...#.....#...#...#...#.......#...#.....#
#.#.#.#.#.#.#.#######.###.#.###.#####.#.#.#.#.###########.#.#.#.#######.#############.#.#.#.###.#.###.#.#.#########.#.#####.#####.###.#####.#
#...#...#.#...#...#...#...#.#...#...#...#.#.#.#...........#...#.......#.........#.....#.#.#.#...#.....#...#.........#.....#.....#.###.#.....#
#########.#####.#.#.###.###.#.###.#.#####.#.#.#.#####################.#########.#.#####.#.#.#.#############.#############.#####.#.###.#.#####
#.........#...#.#.#.###.#...#.....#.#...#...#...#...#...#...#.........#.....#...#.....#.#.#.#...#.........#...#...........#...#.#...#.#.....#
#.#########.#.#.#.#.###.#.#########.#.#.#########.#.#.#.#.#.#.#########.###.#.#######.#.#.#.###.#.#######.###.#.###########.#.#.###.#.#####.#
#.#.....#...#.#.#.#...#...#.........#.#.#.........#...#...#.#.......#...###...#...#...#...#.....#.###...#...#.#.............#.#...#...#...#.#
#.#.###.#.###.#.#.###.#####.#########.#.#.#################.#######.#.#########.#.#.#############.###.#.###.#.###############.###.#####.#.#.#
#.#...#...###...#.....###...#...#.....#...#################......S#...#...#...#.#.#.........#.....#...#.....#.#...............#...#.....#.#.#
#.###.###################.###.#.#.#####################################.#.#.#.#.#.#########.#.#####.#########.#.###############.###.#####.#.#
#...#...###...#...###.....#...#...#...#############################...#.#...#.#.#.#.....###...#...#...........#...#...###...###.#...#...#...#
###.###.###.#.#.#.###.#####.#######.#.#############################.#.#.#####.#.#.#.###.#######.#.###############.#.#.###.#.###.#.###.#.#####
#...#...#...#...#.....#...#.#.......#.#######################.......#.#.....#.#.#.#...#.#...###.#.#.............#...#.....#.....#.....#.#...#
#.###.###.#############.#.#.#.#######.#######################.#######.#####.#.#.#.###.#.#.#.###.#.#.###########.#######################.#.#.#
#.....###.......#...#...#...#.......#.#.....#################...#...#.....#.#...#.....#...#.....#.#.#.........#.........................#.#.#
###############.#.#.#.#############.#.#.###.###################.#.#.#####.#.#####################.#.#.#######.###########################.#.#
###...#...#...#...#...#.............#...#...#E###...#####...###...#.#.....#.............#.......#.#...#.......###...#...#...#...#...#...#.#.#
###.#.#.#.#.#.#########.#################.###.###.#.#####.#.#######.#.#################.#.#####.#.#####.#########.#.#.#.#.#.#.#.#.#.#.#.#.#.#
#...#...#...#.#.......#.................#.....#...#...#...#...###...#.###...#...#...###...###...#...###.....#...#.#...#.#.#...#...#...#...#.#
#.###########.#.#####.#################.#######.#####.#.#####.###.###.###.#.#.#.#.#.#########.#####.#######.#.#.#.#####.#.#################.#
#.#...#.....#...#...#...#.........#.....#.....#.#...#.#.....#.#...#...#...#.#.#.#.#.......#...#...#.........#.#.#.#.....#...#.......#...#...#
#.#.#.#.###.#####.#.###.#.#######.#.#####.###.#.#.#.#.#####.#.#.###.###.###.#.#.#.#######.#.###.#.###########.#.#.#.#######.#.#####.#.#.#.###
#.#.#.#...#.......#...#...#.....#...#...#.#...#.#.#...#...#.#.#...#...#...#.#.#...#...#...#.....#.........#...#...#.#.......#.....#.#.#.#...#
#.#.#.###.###########.#####.###.#####.#.#.#.###.#.#####.#.#.#.###.###.###.#.#.#####.#.#.#################.#.#######.#.###########.#.#.#.###.#
#.#.#.....###...###...#.....###.......#...#.....#...#...#...#...#.#...#...#.#...#...#...#.......###.......#.#.....#.#.#...#...#...#...#.....#
#.#.#########.#.###.###.###########################.#.#########.#.#.###.###.###.#.#######.#####.###.#######.#.###.#.#.#.#.#.#.#.#############
#...#...###...#.....#...###.............#.......#...#.......#...#.#...#...#.#...#.......#.....#...#...#.....#...#.#...#.#...#.#.....#...#...#
#####.#.###.#########.#####.###########.#.#####.#.#########.#.###.###.###.#.#.#########.#####.###.###.#.#######.#.#####.#####.#####.#.#.#.#.#
#.....#.....#.....#...#...#.........###.#.#...#...#.....#...#...#...#.....#...#.........#.....#...#...#.#.......#.....#.....#.#...#.#.#.#.#.#
#.###########.###.#.###.#.#########.###.#.#.#.#####.###.#.#####.###.###########.#########.#####.###.###.#.###########.#####.#.#.#.#.#.#.#.#.#
#...........#.###.#.#...#.........#...#...#.#...###...#...#.....###...........#.......#...#...#...#.....#.........###.......#...#...#.#.#.#.#
###########.#.###.#.#.###########.###.#####.###.#####.#####.#################.#######.#.###.#.###.###############.###################.#.#.#.#
###.........#.#...#.#...#...#...#.#...#...#.#...#...#.....#...#...###...#...#.#.......#.....#.#...#...#.........#.........###...###...#.#.#.#
###.#########.#.###.###.#.#.#.#.#.#.###.#.#.#.###.#.#####.###.#.#.###.#.#.#.#.#.#############.#.###.#.#.#######.#########.###.#.###.###.#.#.#
#...#...#...#.#.....###...#...#.#.#...#.#.#.#...#.#.....#.#...#.#.#...#.#.#...#.....#...#.....#...#.#.#.......#.#...#...#...#.#...#...#...#.#
#.###.#.#.#.#.#################.#.###.#.#.#.###.#.#####.#.#.###.#.#.###.#.#########.#.#.#.#######.#.#.#######.#.#.#.#.#.###.#.###.###.#####.#
#.....#...#...#...#######...#...#.....#.#.#.#...#...#...#.#.###.#.#...#.#.....#.....#.#.#.....#...#.#.###...#.#.#.#.#.#.....#.#...#...#...#.#
###############.#.#######.#.#.#########.#.#.#.#####.#.###.#.###.#.###.#.#####.#.#####.#.#####.#.###.#.###.#.#.#.#.#.#.#######.#.###.###.#.#.#
#...#...#.......#...###...#...#...#...#.#...#.#.....#.#...#...#.#...#.#.#...#.#...#...#.#...#.#...#.#.#...#...#...#.#.........#.....#...#.#.#
#.#.#.#.#.#########.###.#######.#.#.#.#.#####.#.#####.#.#####.#.###.#.#.#.#.#.###.#.###.#.#.#.###.#.#.#.###########.#################.###.#.#
#.#...#.#.....#...#...#.........#...#.#...#...#...#...#...#...#.#...#.#.#.#...#...#.#...#.#.#...#.#.#.#...........#...#...#...#...#...###...#
#.#####.#####.#.#.###.###############.###.#.#####.#.#####.#.###.#.###.#.#.#####.###.#.###.#.###.#.#.#.###########.###.#.#.#.#.#.#.#.#########
#.#...#.......#.#...#...#...###.......#...#...#...#...#...#...#.#.....#.#.....#.#...#.....#.#...#...#...#.....#...#...#.#.#.#...#.#.........#
#.#.#.#########.###.###.#.#.###.#######.#####.#.#####.#.#####.#.#######.#####.#.#.#########.#.#########.#.###.#.###.###.#.#.#####.#########.#
#.#.#...#...#...###...#...#.....#.....#.....#.#.#...#.#.....#.#.###.....#...#.#...#.........#.......#...#.###...###.....#.#.....#...#.....#.#
#.#.###.#.#.#.#######.###########.###.#####.#.#.#.#.#.#####.#.#.###.#####.#.#.#####.###############.#.###.###############.#####.###.#.###.#.#
#.#.#...#.#.#...#.....#...#.....#.###...#...#.#...#.#.#.....#...#...#...#.#.#.....#...#.......#...#.#...#.....#.........#.#...#...#...###...#
#.#.#.###.#.###.#.#####.#.#.###.#.#####.#.###.#####.#.#.#########.###.#.#.#.#####.###.#.#####.#.#.#.###.#####.#.#######.#.#.#.###.###########
#...#...#.#.....#.....#.#...###.#.....#.#...#...#...#.#.###.......#...#.#.#.#...#.#...#.#.....#.#...###.#...#...#...#...#.#.#...#...........#
#######.#.###########.#.#######.#####.#.###.###.#.###.#.###.#######.###.#.#.#.#.#.#.###.#.#####.#######.#.#.#####.#.#.###.#.###.###########.#
#.......#.#...#.......#.###.....#.....#.#...#...#.#...#...#.......#.###...#.#.#...#.....#.....#.......#.#.#.#...#.#...###.#...#.#...........#
#.#######.#.#.#.#######.###.#####.#####.#.###.###.#.#####.#######.#.#######.#.###############.#######.#.#.#.#.#.#.#######.###.#.#.###########
#.#.......#.#.#.......#.#...#...#...#...#.#...#...#...#...#.......#...#.....#...........#.....#...#...#...#.#.#.#.#...#...#...#.#...........#
#.#.#######.#.#######.#.#.###.#.###.#.###.#.###.#####.#.###.#########.#.###############.#.#####.#.#.#######.#.#.#.#.#.#.###.###.###########.#
#...#.......#.........#.#...#.#...#.#.#...#.#...#...#.#...#.#...#...#.#...#...#...#...#.#.#...#.#...#...#...#.#.#...#.#.....###.....#.....#.#
#####.#################.###.#.###.#.#.#.###.#.###.#.#.###.#.#.#.#.#.#.###.#.#.#.#.#.#.#.#.#.#.#.#####.#.#.###.#.#####.#############.#.###.#.#
#.....#...#...........#...#...#...#.#.#.#...#...#.#...#...#.#.#.#.#.#...#.#.#...#.#.#...#...#.#.....#.#.#.#...#.#...#...........###...#...#.#
#.#####.#.#.#########.###.#####.###.#.#.#.#####.#.#####.###.#.#.#.#.###.#.#.#####.#.#########.#####.#.#.#.#.###.#.#.###########.#######.###.#
#.#...#.#.#.#.........#...###...#...#.#.#.#...#.#...#...###...#.#.#.#...#.#...#...#.#.........#.....#.#.#...#...#.#...#...#...#.......#.....#
#.#.#.#.#.#.#.#########.#####.###.###.#.#.#.#.#.###.#.#########.#.#.#.###.###.#.###.#.#########.#####.#.#####.###.###.#.#.#.#.#######.#######
#...#...#...#.........#.#.....#...#...#.#...#...###.#.....###...#.#.#...#...#.#...#.#.....#...#.......#.....#.#...#...#.#.#.#...#...#.......#
#####################.#.#.#####.###.###.###########.#####.###.###.#.###.###.#.###.#.#####.#.#.#############.#.#.###.###.#.#.###.#.#.#######.#
#.....................#.#...#...###...#.#...#.......#...#...#.#...#...#.#...#...#.#...###...#...#...#...#...#.#...#...#.#.#...#.#.#.#.....#.#
#.#####################.###.#.#######.#.#.#.#.#######.#.###.#.#.#####.#.#.#####.#.###.#########.#.#.#.#.#.###.###.###.#.#.###.#.#.#.#.###.#.#
#.........#...#...#...#.###.#...#.....#...#.#.....#...#.#...#.#.....#.#.#...#...#.#...#.........#.#...#.#...#.#...#...#.#.#...#.#.#...###.#.#
#########.#.#.#.#.#.#.#.###.###.#.#########.#####.#.###.#.###.#####.#.#.###.#.###.#.###.#########.#####.###.#.#.###.###.#.#.###.#.#######.#.#
#.........#.#...#...#.#.#...#...#.......#...#.....#...#.#...#.#.....#.#.#...#...#.#...#.#.......#.....#.#...#...###...#.#.#.#...#.......#.#.#
#.#########.#########.#.#.###.#########.#.###.#######.#.###.#.#.#####.#.#.#####.#.###.#.#.#####.#####.#.#.###########.#.#.#.#.#########.#.#.#
#.....#.....#.........#.#.#...#.........#.#...#...#...#.#...#.#.....#.#.#.......#.#...#...#.....#.....#.#.....#...#...#.#.#.#...#.......#.#.#
#####.#.#####.#########.#.#.###.#########.#.###.#.#.###.#.###.#####.#.#.#########.#.#######.#####.#####.#####.#.#.#.###.#.#.###.#.#######.#.#
#.....#.#.....#...#...#.#.#...#.#...#...#.#.#...#.#.#...#.#...#...#.#.#.....#.....#.....#...#...#.....#.#...#...#.#...#.#.#.#...#.......#.#.#
#.#####.#.#####.#.#.#.#.#.###.#.#.#.#.#.#.#.#.###.#.#.###.#.###.#.#.#.#####.#.#########.#.###.#.#####.#.#.#.#####.###.#.#.#.#.#########.#.#.#
#.......#.......#...#...#.....#...#...#...#...###...#.....#.....#...#.......#...........#.....#.......#...#.......###...#...#...........#...#
#############################################################################################################################################
"""


if __name__ == "__main__":
    race_track = RaceTrack.parse(INPUT).init()
    print("Race track ready for analysis.")
    print(
        "Number of cheats (length <= 2) saving at least 100 picoseconds:",
        sum(
            1
            for cheat, saving in race_track.iter_cheats(2, tqdm=tqdm)
            if saving >= 100
        )
    )
    print(
        "Number of cheats (length <= 20) saving at least 100 picoseconds:",
        sum(
            1
            for cheat, saving in race_track.iter_cheats(20, tqdm=tqdm)
            if saving >= 100
        )
    )
