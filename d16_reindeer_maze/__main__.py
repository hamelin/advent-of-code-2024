from . import *  # noqa


INPUT = """\
#############################################################################################################################################
#.............#.........#...#...#.......#.......#.............#.....#.....................#.........#...................#.........#...#....E#
#.#.#####.###.#.#.#####.#.#.#.#.#.###.###.#.#.###.###.#######.#.###.#####.#####.#######.#.#.#######.#.#.###.###########.#.#########.#.#.#.#.#
#.#.#.....#.....#...#.....#.#.......................#.#...#...#.#.#.#...#.#...#.........#.#.#.....#.#.#.#...........#...#.#.......#.#...#.#.#
###.#.###.#.#######.#######.#########.###.#.#.#######.###.#.###.#.#.#.#.#.#.#.#.#.#####.#.#.#.###.#.###.#.#.#####.###.###.#.#####.#.#####.#.#
#...#...#...#.....#.#...#.............#...#.#.....#...#...#.....#.#...#.#.#.#.#.......#.#.#...#...#...#.#.....#.#...#...#.#...#.#.#.#.....#.#
#.#.###.#.###.#####.#.#.#############.#.#.#.#####.#.###.#.#######.###.#.###.#.###.#.###.#.###.#.#####.#.###.#.#.###.###.#.###.#.#.#.#.###.#.#
#.#.#...#.....#...#.#.#...#.........#...#.#.......#.#...#...#.........#.#...#.....#.#...#...#.#.#.......#...#...#.#.....#...#.#.#.....#.#.#.#
#.###.#.#.###.#.#.#.#.###.###.#####.#.###.#########.#.#####.#######.#.#.#.#######.#.#.#.###.###.###########.###.#.#######.###.#.#######.#.#.#
#.#.......#...#.#.#.....#...#.#...#.....#.....#.........................#...#...#.#.#.#...#...#.......#.....#...#.................#...#...#.#
#.#.###.#.###.#.#.#.#####.#.#.###.#.#.#######.#.#.#.#.###.#.#.###.###.#.#.#.#.#.#.###.#.#####.#.#####.#.#.###.#########.#########.#.#.###.#.#
#...............#.#.#...#.#.#.#...#.........#...#...#...#.#...#.......#.#.#...#.#.....#.....#.#.#...#.#.#.............#.#.......#.#.#.......#
#.###.#.#.#.#.###.###.#.###.#.#.#########.###############.#####.#####.#.#######.#.#.#.#.#.###.#.#.#.#.###############.#.#.#####.#.#.#####.#.#
#...#...#...#...#.....#...#.#.#.....#...#.....#...........#...#.#.............#.#...#.............#.#...........#...#.#.#...#...#.#.#.......#
###.###.#####.###########.#.#.###.#.#.#.#####.#.#####.#.###.#.###.###.#######.#.#.#####.###.#######.###########.#.###.#####.#.###.#.#######.#
#...#.#...#.......#.....#...#.....#.#.#.........#.#...#.#...#.#...#...#.....#...#.....#...#.#...#.#...#.....#.#.#.....#...#.#...#.#.#.....#.#
#.###.###.###.#.###.#.###.#####.#####.#####.###.#.#.#####.###.#.###.#.#.###.###.#####.#.#.#.#.#.#.###.###.#.#.#.#.#####.#.#.###.#.#.#.###.#.#
#.#.....#...#.#...#.#.......#...#.....#.....#...#.#.......#.#...#...#...#.#...#.#...#.....#.#...#.........#.#.#.....#...#.....#.#.#...#...#.#
#.#####.#.#.#.###.#.#####.#.#####.#####.#####.###.#########.#####.#######.###.###.#.#######.#.#.#####.#####.#.#.###.#.#######.#.#######.###.#
#.........#.....#.......#.#.......#...#.#...#.....#...#.........#.#.......#...#...#.......#.#.#.........#.....#...#...#...#.....#.........#.#
#.#######.#####.#########.#########.#.#.#.#.###.#.#.###.#.#######.#.#####.#.###.#######.#.#.#.#########.#####.###.#####.###.#####.#######.#.#
#...............#.........#.......#.#...#.#.#.....#.....#...#...#.#.#.....#.#.......#...#.....#.......#...#...............#...#...#.........#
###.#####.#####.#.###.#.###.#####.#.#####.###.#####.#######.#.#.#.#.###.#.#.#####.#.#.#####.#.#.#####.###.#########.#####.###.#.#.#.###.#.#.#
#...#...#.....#.#...#.#.#.....#...#.#.....#...#...#.#.#.....#.#.#.#.#...#.#.....#.#.#.....#.#...#...#.#.#...#.....#.#.....#.#.#.#.....#.#.#.#
#.#.#.###.###.#.#.###.#.###.#.###.#.###.#.#.###.###.#.#.###.#.#.#.#.#.#.#.#####.###.#####.#.#####.#.#.#.###.#.###.#.#.###.#.#.#########.#.#.#
#...#...........#.#...#...#.#...#.#...#.#.#.#.....#.#.#.....#.#...#...#.#.....#.....#...#.#.......#...#.....#...#...#.#.....#.....#...#.#...#
#.#.#####.#######.#.#####.#.###.#.###.###.#.#####.#.#.#####.#.#######.#.#######.#######.#.#######.#####.#######.#####.###########.#.#.#.###.#
#.#.....#...#.....#.#.....#...#.#...#.....#.....#...#...#...#.#.....#.#.......#.........#.#...#.........#.......#.....#...#.....#...#.#.....#
#.#####.#.#.#.#####.#.#.#######.#.#.#####.#####.#.###.###.#.#.#.###.###.#####.#.#####.###.#.#.#.#########.#####.#.###.#.#.#.#.#######.#####.#
#.....#...#...#.....#.#...#.....#.#.....#.....#.#...#.#...#.#.....#...#.....#.#...#.#...#.#.#...#.....#...#.#.....#...#.#...#.......#...#...#
#####.###.#####.#.###.###.#.#####.###.###.#####.###.#.#.#############.#######.###.#.###.#.###.#.#.###.#.###.#.#.#.#.###.###########.###.#.#.#
#...#...#.......#.#.....#.#.........#.....#...#.#.#...#.......#.............#.......#...#...#.#...#.#...#.....#.#.#.....#.........#...#.#.#.#
#.#####.#.#####.#.#######.#####.#######.###.#.#.#.#.#######.###.###.#######.#########.#.###.#.#####.###########.#.#######.#######.#.###.#.#.#
#.#.....#.....#.#.......#.#...#...#.........#...#.#.#.......#...#.........#.....#.....#.#...#...................#.#.#.....#.....#.#...#...#.#
#.#.#####.###.#.#######.#.#.#.#####.#####.#######.#.#.#####.#.#.#.#######.###.#.#.#####.#.###.#.#.#########.###.#.#.#.#.###.#.###.###.#####.#
#.#.#.....#.#.....#.#...#.#.#...#...#...............#.....#.#.#.#.......#...#.#.#.#.#...#...#.#.#.#.......#.#...#.#...#.#.....#...#.........#
#.#.#####.#.#####.#.#.###.#.###.#.###.###########.###.#.###.#.#.#.#####.###.###.#.#.#.#####.###.###.#####.#.#.#.#.#####.###.#.#.###.###.#.#.#
#.#.......#.#...........#...#.#...#...#.........#.#...#.....#.#.#...#...#.#.....#.#.......#...#.....#...#...#.#.#.#...#...#.#.....#.#...#.#.#
#.#########.#.#####.###.#.###.#.#######.#######.#.#.#########.#####.#.###.#######.#.###.#.#.#.#.#######.###.#.#.#.#.#.###.#.#######.#.###.#.#
#.....#.......#...#...#.#.#...........#...#.....#.#.#.....#...#...#.#.#...........#...#.#.....#.#.........#...#.#...#.#...#.#...#...#.#.#...#
#.###.#.#######.#.#####.#.#####.###.#.###.#.#######.#.###.#.###.#.#.#.###.#.#######.#.###.#####.#####.#.#######.#####.#.###.#.#.#.#.#.#.#####
#.#...#.#.....#.#...#...#.......#.....#...#.#.....#...#...#.....#...#...#.#.#.......#.....#...#.#.....#.#.....#.....#...#.#.#.#.#.#.#.......#
#.#####.#.###.#.###.#.###########.#####.###.#.###.###.#.#.#######.#.###.#.#.#.#############.#.#.#.#######.###.###.#.#####.#.#.#.#.#.#######.#
#.#.....#.#...#.#.#.#.....#...#.#.#.....#.#...#.#...#.#...#.....#.#.....#.#.#.#.......#.....#...#.......#...#.....#...#...#...#.#.#.....#.#.#
#.#.#####.#####.#.#.#.###.#.#.#.#.#.###.#.#####.###.###.#.###.#.#.#.###.#.#.#.#######.#.#########.#####.###.#######.###.#.#.#####.#####.#.#.#
#.#.......#...#.#.#.#.#.#.#.#...#...#.............#...#.#.....#.#.#.#...#.#.#.......#.....#...#.....#.....#...#.....#...#...#...#.........#.#
#.#####.###.#.#.#.#.#.#.#.#.#########.#########.#####.#.#######.#.#.#.#####.#######.#####.#.#.#.#####.###.###.#####.#.#######.#.#.#.#####.#.#
#.#...#.#...#.#.#...#...#.#.#.......#...#.#...#.#.....#...#.#...#...#.....#.......#...#...#.#...#...#.#.....#.#...#.#.....#...#.#.#.........#
#.#.#.#.#.###.#.###.#####.#.#.###.#.###.#.#.#.#.#.#######.#.#.###########.#####.#.###.#.###.###.#.#.#.#######.#.#.###.#####.###.#.###.#.#.#.#
#...#.#.#...#.#...#.#.....#...#.#.#.....#...#...#.........#.#...........#.#.....#.#...#...#...#...#.#.#.....#...#.....#...#.#.#...#.#.#.#...#
#.###.#.###.#.###.#.#.#####.###.#.#####.#######.###########.#######.#####.#.#######.#####.###.#####.#.#.###.###.#######.#.#.#.#####.#.#.#.###
#.#...#.#.#.#.....#...#...#.#...#.#.....#.....#...#.......#.....#...#.....#...#...#.....#.#...#...#...#.#.#...#...#...#.#...#.........#.#...#
#.#.###.#.#.#.#########.#.#.#.#.#.#####.#.###.#####.###.###.#.#.#.###.#####.#.#.#.#####.#.#.#.#.#.###.#.#.###.###.#.#.#.#####.#######.#.#.###
#.#.....#.#.#...#.....#.#...#.#.#.....#.#.#.#.....#...#...#.#...#.#...#.....#.#.#...#...#...#.#.#.....#.#...#...#...#.#.#.....#.....#.#.#...#
#.#######.#.###.#.#.#.#.#####.#######.#.#.#.#####.###.###.#.#.###.#.###.#####.#.###.#.#####.###.#####.#.#.#####.#.#####.#######.###.###.#.#.#
#.....#...#...#...#.#.#.#.....#...#...#.#.#.....#.#...#.#.#.#.#...#.#.#...#.#...#.#.#...#...#...#...#...#...............#.....#.#.#.....#.#.#
#####.#.#.###.#####.###.#.#.###.#.#.#####.###.###.#.###.#.#.#.#.###.#.###.#.#.###.#.###.#.###.###.#.#####.#############.#.###.#.#.#########.#
#...#...#.#...#...#.......#.#...#.#.....#.....#...#...#.#...#.#.#.#.#...#.#.......#.#...#.....#...#.........#.....#.....#...#...#.....#.....#
#.#######.#.###.#.#.#########.###.#####.#####.#.###.#.#.#####.#.#.#.#.###.#.#.###.#.#.###.#.#.###.#.#########.###.#########.#####.#.#.#.###.#
#...#...#.#.#...#.#...#.......#...#.....#...#.#.#...#.#.....#...#.#.#...#.#.#.#.#.#...#.....#...#...#.......#.#.#...........#.....#.#...#.#.#
###.#.#.#.#.#.###.###.#.#########.#.###.###.#.#.#.#.#.#.#######.#.#.#.#.#.###.#.#.#############.#.###.#####.#.#.#############.#####.#####.#.#
#...#.#.#.#.#.#.#...#.#.....#...#...#...#...#.....#...#.....#.....#.#.#.......#.#.#...........#.#...#.#...#...#...........#.#.#.#...#.....#.#
#.###.#.#.#.#.#.###.#.#####.#.#.#######.#.###.#############.#.#.#.#.###########.#.#.#.#.#####.#.###.#.#.#.#############.#.#.#.#.#.#####.###.#
#...#.#...#.......#.#.#...#.#.#.......#...#...#...........#...#...#...#...#.......#...#.#.#...#.#.#.#...#.#.........#...#.#.....#...#...#...#
#.#.#.###########.#.#.#.#.#.#.#.###.#.###.#.###.#######.#.#.###.#####.#.#.#.#######.#.#.#.#.###.#.#.#####.###.#####.#.###.#.#######.#.###.###
#.#.....#.......#.#...#.#...#...#...#.#...#...#...#.....#.#...#.#...#...#.#...#.....#...........#.......#.....#.#...#.#.#.#.#.....#.#.....#.#
#.#######.#####.###.#.#.###.###.#.#.#.###.###.###.#.#####.#.###.#.#.#####.###.#####.###################.#####.#.#.###.#.#.#.#.###.#.#.#####.#
#.#.#.....#...#.....#.#...#...#...#.#...#...#.....#.......#.#...#.#.......#.#.....#.......#.......#.......#.....#.....#...#.#...#...#.#...#.#
#.#.#.#######.#######.###.###.#####.###.###.#######.#######.#.#.#.#########.#####.#.#.###.#.#####.#########.###.###.###.#.#####.#####.#.#.#.#
#...#.....#.....#.....#.#.#.....#...#.#.#...#.#.....#...#...#...#.............#...#...#.#.#.....#.........#.#...#...............#.#...#.#...#
#####.#.#.#.###.###.#.#.#.###.###.###.#.###.#.#.#####.#.#.###.#.#####.#.#.###.#.#####.#.#.#.###.#######.#.#.#.#.#.#.#############.#.###.#####
#...#...#.#...#...#.#...#...#.#...#...#...#.......#...#.#.#...#.....#...#.#.#...#...#...#.#.........#...#...#.#...#.......#.................#
#.#.###.#.###.###.#.###.###.###.###.#####.#######.#.###.#.#.#####.#######.#.#####.#.###.#.#########.#.#######.#.#########.#.#.#.#.###.#.###.#
#.#.....#.....#.......#.#.....#...#...#...#.......#.#.#.#.#.#.#...#.....#...#.#...#.....#.....#.....#.......#...#.....#...#.#.#...#.#.#...#.#
#.#####.#.#.###.###.#.#.#.###.###.#.#.#.#.#.#######.#.#.###.#.#.###.#.#.###.#.#.#.###.###.#####.#######.#########.#.#.#.#.#.#.###.#.#.#.###.#
#.....#...#.#.......#.#.#...#...#.#.#.#...#...#.....#.#.......#...#.#.....#.#...#.#.#.#...#...#.#.....#...#...#.....#...#.#.#.#...#.#.#.#...#
#####.#.###.###########.#.#.#.###.#.#.#.#####.###.###.#######.#.###.#.#####.#.###.#.#.#.###.#.#.###.#.#.#.#.#.#.#.#.#.#.###.#.###.#.#.###.#.#
#.....#.#.......#.......#.#.#.....#.#.#.....#...#...#.......#...#...#.......#.#...#...#.....#.#...#.#.#.#.#.#...#.#...#...#.#...#...#.....#.#
#.#####.#.#####.#.#######.#.#########.#####.###.###.#.#######.###.###########.#.#.###.#######.###.#.#.#.#.#.#####.#.#####.#.###.###.#######.#
#.#.....#.#...#...#.......#.............#.#...#...#.......#.....#.#.....#.....#.#...#.#.........#...#.#.#.#.#.#...#.....#...#...#.#.....#...#
#.#.#####.#.#.#####.#######.###########.#.#.#.###.#.###.#.#.#####.#.###.#.#####.###.#.#.#######.#####.###.#.#.#.#.###########.###.#####.#.###
#.#.........#.#.......#.....#...#.....#...#.#...#.#...#.#.....#.......#.#.......#...#...#...#...#...#...#.#...#.#.#.........#.#.........#...#
#.#.#########.#########.#####.#.#.###.###.#.#####.###.#########.###.#.###.#.#####.#######.#.#.###.#.###.#.###.#.###.###.###.#.#######.#####.#
#.#...#.#...#.........#.#.....#.....#.#.#.#.........#.#...........#.#.....#.#...#...#...#.#...#...#...#.#.....#.....#...#...#.......#.#.....#
#.###.#.#.#.#########.#.#.###.#######.#.#.#####.###.#.#.#########.#.#######.#.#.###.#.#.#.#########.#.#.###.#######.#.#############.#.#.#####
#.#...#.#.#...#...#...#.#...#...#.....#.#.....#...#...#.#.........#.#.........#.#.....#.#.#.........#.#...#.#.....#.#...............#.#.....#
#.#.###.#.###.#.#.#.###.###.#.#.#.#####.###.###.#####.#.#.#.#####.#.#.#########.#.###.#.#.#.###.#########.###.###.#.#############.#.#.#####.#
#.#.....#.#.#.#.#.#.....#.#...#.#.#.........#...#.....#.#.#...#.#.#.#...#...#...#.#.......#...#.........#.....#...#.............#.#.....#...#
#.#######.#.#.#.#######.#.###.###.#.#####.#.#.#.#.#####.#.###.#.#.#.#.###.#.#.#.#.#####.#####.#########.#######.###.###.#.###.###.###.###.###
#...#...#...#.#.......#...#...#...#.....#.#.#.#.#.#.#...#...#.#.#.#...#...#...#.#.....#...#...#...............#.#.#.#...#...#...#...........#
###.#.#.###.#.#######.###.#.#.#.###.###.###.#.###.#.#.#######.#.#.#.###.#######.#####.###.#####.###############.#.#.#.#.#######.#.#.#.#####.#
#...#.#.#...#.......#.....#.#.#.#...#.#.....#.#...#.#...#.....#...#.....#.....#.#.#...#.#...#...#.........#.....#...#.#.........#.#.#.......#
#.###.#.#.#.#######.#.#####.#.#.#.###.#######.#.###.###.#.#####.#########.###.#.#.#.###.###.#.###.#######.#.#####.###.#####.#####.#.#.###.###
#.....#.........#...#...#...#.#.#.....#.....#.........#.#.....#...#...#.....#.#.#.#...#.#.....#...#...#...#.#.......#...#...#.....#.........#
#.###############.#######.###.#.###.#.#.###.#####.#####.#####.###.#.###.###.###.#.###.#.#.#.###.###.#.#.###.#.#####.###.#.###.#####.#.#####.#
#.....#...#.....#.......#.#...#...#.#...#.....#.......#.....#...#...#.....#...#.#.#...#...#.......#.#.#...#.#.#...#.#...#.....#...#.........#
#####.#.#.#.###.#.#####.#.###.###.#.#.###.#.###.#####.#####.###.###.#.#######.#.#.#.#####.#.###.###.#.###.#.###.#.#.#.#####.#####.###.#####.#
#.#...#.#...#.#.#.#.....#...#.#...#.#.....#.#...#...#...#...#.......#.#.......#...#.....#.#...#.....#.....#.#...#.....#.....#.....#.......#.#
#.#.#.#.#####.#.#.#.###.###.#.#.###.#####.###.#.###.#.###.###.###.#.#.#.#####.###.#####.#.#.###.###.#######.#.###.#####.#####.###.#.#.###.#.#
#...#...#.....#...#.#.#.#.#...#.#.......#.#...#.....#.....#.....#...#.#.....#.#...#...#.#.#.#...#...#...#...#...........#.....#...#.#.....#.#
#.###.###.#######.#.#.#.#.###.#.#.###.#.#.#.#####.#########.###.#####.#####.###.###.#.#.###.#.#######.#.#.###.#############.###.###.#.###.#.#
#.................#.#.......#.#.#.#...#...#.....#.....#...#...#.......#...#.......#.#.#.....#.#.......#.#...#...#...........#.#.....#...#.#.#
#.#.#.#########.#.#.#.#######.#.###.#.#########.#.#.#.#.#.###.#####.###.#.#.#.###.#.#.#######.#.#######.###.#.#.#.#.#####.#.#.#.#####.#.###.#
#...#.........#...#.#.#.......#.#...#...............#...#.#.#.#.....#.#.#.#.#...#.#.#...#...#.#.......#...#.#.#.#.#.#...#...#...#.....#.....#
#####.#######.#.###.#.#.#######.#.#################.#####.#.#.#.###.#.#.#.###.###.#.###.#.###.#######.#.###.###.#.#.#.#.#########.###.#######
#...#.......#.#.....#.#.#.....#.#.#.................#.......#.#...#...#.#.....#...#...#.#.#.....#.........#.#...#.#...#.#...#.....#.#.......#
#.#.#########.#####.###.#.#.#.#.#.###.#.###.#########.#######.#.#.###.#.###.###.###.#.#.#.#.###.#.#######.#.#.###.#####.#.#.#.###.#.#.#####.#
#.#.....#.....#...#.#.....#.#.#.#...#.#.#...#.....#.......#...#.#.....#.#.....#.#.....#.#.#.#...#.#.....#...#.#.#...#.#.#.#.#.#.....#.#.#...#
#.#####.#.#####.###.#.#####.#.#.###.###.###.#.###.#########.#########.#.#.###.#.#####.#.#.#.###.#.#.###.#####.#.###.#.#.#.#.#.#.#.###.#.#.#.#
#.#...#.#.....#...#.#.....#.#.#...#...#...#.#.#.#.........#.....#...#.#...#.#...#.....#.#.#...#.#.#.........#.#.....#.#...#...#.#.....#.#.#.#
#.#.#.#.#####.#.#.#.#####.#.#####.###.###.###.#.#########.#####.#.#.#.#####.#####.#####.#.###.###.#.#.#####.#.###.###.#.#.#####.#.#####.#.###
#.#.#.#.......#.#.....#...#.....#...#.#...#...#.......#.....#...#.#...#.........#...#.....#...#.....#...#.#.#...#.....#...#...#...#.....#...#
#.#.#######.#########.#.#######.#.###.#.#.#.###.#.#####.#####.###.###.###.#.###.###.#####.#.###.###.###.#.#.###.#####.#######.#.#.#####.###.#
#.#.........#.....#...#.......#.#...#.#.....#...#.#...#.......#.#...#...#.#...#.#.......#.#...#.#.....#.#.....#...#.#...#.....#...........#.#
#.#.#########.###.#.#.#####.#.#.###.#.#.#####.#.###.#.#.#.#####.#.#.#.#.#####.#.#.#.#.#.#####.#.#######.#.###.###.#.###.#.#######.#####.###.#
#.#.#.........#.#.#.#.......#...#.#...#.#.....#.#...#.#.#.#.....#.....#.....#.#...#.#.#.....#.#.#.....#...#.#.....#...#.#...........#...#...#
#.###.#########.#.###.###.#####.#.#####.#.#.#####.###.#.#.#.###.#.###.#.###.#.#######.###.###.#.#.###.###.#.#######.#.#.#.#######.#.#.#.#.###
#...#.#.....#...#.......#.#.....#...#...#.#.........#.#...#.#...#...#.....#.............#...#.#...#.#.....#.......#.#.#.#.....#...#.....#...#
#.#.#.#.###.###.#########.#.#######.#.###.#########.#.#####.#.#####.#####.#.#####.#.#######.#.#####.###########.#.#.###.###.###.#.#####.###.#
#.#...#.#.#.....#.....#...#.#.#.....#.#...#.#.....#.#.........#.......#...#.....#.#...#.....#.........#.........#...#...#...#...#...........#
#.#####.#.###.###.#.#.#.###.#.#.#.###.#.###.#.###.#.#######.#.#.#######.#######.#.#.###.###.###.#.#.###.#.#########.#.#######.###.#####.###.#
#.......#.....#...#...#.....#.#.#.....#.#...#.#...#.#...#...#.#.#...#...#...#...#.#...#...#.#.#...#.#...#.....#.....#.......................#
#.#.###########.#.#.#########.#.###.###.###.#.#.###.#.#.#.#####.###.#.###.#.#.###.###.###.#.#.#####.#.#######.#.###############.#######.#.###
#.#.......#.....#.#...............#...#...#.#.#...#.#.#.#.........#.#.....#.#.#.......#.#.#...#...#.#.......#.#.#.........#...#...........#.#
#.#######.#.#####.#######.###.###.#.#####.#.#.###.#.###.#########.#.#######.#.#######.#.#.###.#.#.#.#######.#.###.#####.#.#.###.###########.#
#.......#...#...#.......#...#.#...#.........#.#...#.....#.....#.#...#...#...#.#.....#.#.#...#...#.#...#.....#...#.#...#.#...#...#...........#
#######.#####.###.#.###.#.#.#.#.###.#########.#.#########.###.#.#.###.#.#.###.#.###.#.#.###.#.###.###.#.#######.#.#.#.#.#####.###.#######.###
#.....#...............#...#.#.#...#.#.......#.#.#.......#.#...#...#...#.............#.#...#.#.#.......#.#...#...#...#.#.....#.#.#...#...#...#
#.#######.#.#.#.#####.#.#.#.#.#.#.#.#.#####.#.#.#.#####.#.#.###.###.#######.#.#.#.#.#.#.#.#.###.#.#####.#.###.#.#.###.#####.#.#.###.#.#####.#
#.#.....#.#.#.#.#...#.#.#...#.#.#.#.#...#.#...#...#...#...#.#.#...#.........#.#.#.#.#...#.#...#.#.#.....#.#...#.....#.#...#...#...#.#.#.....#
#.#.###.#.#.#.#.###.#.###.###.#.#.#####.#.#########.#######.#.#.###.#.#.###.#.#.#.#.#########.#.#.#.#####.#.#####.#.#.###.#######.#.#.#.###.#
#.#...#.#.#.#.#.....#.#...#.....#.......#...#.....#.......#.#...#...#.#.#.....#.#...................#.....#.#.#.....#...#.......#.....#...#.#
#.###.#.#.#.#######.#.#.#.#####.#########.###.###.#.#####.#.###.#.###.#.#.#####.###.#####.#.#####.#.#.#.###.#.#.#.#####.###.###.#.#######.###
#...#.#...#...#.....#.#.#.....#.........#.....#.#.#.#...#.#...#.#...#...#.........#.......#...........#.#...#...#...#...#...#...#.#.....#...#
#.###.#######.#.#####.#.#.###.#.#####.###.#####.#.#.#.#.#.###.#####.###.#####.###.#####.###.#####.###.#.#.###.#####.#.###.###.#####.###.###.#
#.....#...................#...#.....#.....#.....#...#.#.....#.#...#...#.....#.#.#.....#...#.........#...#...#.#.....#.#...#...#.....#...#...#
#.#####.###.#.#.#.###.#####.###.###.#.#.###.###.#####.#######.#.#.###.#####.#.#.#####.###.###.#########.#.#.#.#.#####.#.###.#####.###.###.###
#.....#.#.#.#...#...#.....#.....#...#.#.#...#.#.....#.........#.#...#.#...#.#...#.....#...#...............#.....#...#...#...#...#.#.#...#...#
#.###.#.#.#.#######.#####.#######.#####.#.###.#####.###########.###.#.#.###.#####.#.###.#######.###.#.#.#.#######.#.#####.###.#.#.#.###.###.#
#S......#...........#...........#.........#.....................#.....#...........#.............#.....#.#.........#...........#...#.........#
#############################################################################################################################################
"""


if __name__ == "__main__":
    maze = Maze.parse(INPUT)
    paths_best = find_paths_cost_minimum(maze)
    assert paths_best
    print(
        "Minimal cost of traversal:",
        paths_best.pop()[-1].cost
    )
    print(
        "Number of spaces on best paths:",
        len(enum_positions_on_paths(paths_best))
    )
