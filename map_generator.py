def map_gen(rows=16, cols=16):
    with open("map2.txt", "w") as f:
        for _ in range(rows):
            f.write(' '.join(['.'] * cols) + '\n')

import random
#TODO: make spacesbeteween each char . horizontally
#TODO: make gen function for caves etc 
def gen_map(x=16, y=16):
    ROWS, COLS = x, y*2
    WALL_PROBABILITY = 0.00  # 5% of tiles are walls
    CAVE_PROBABILITY = 0.005 # 0.5%
    MOUNTAIN_PROB = 0.2 # 0.50%
    TREASURE_PROB = 0.001 # 0.01

    # Generate the map as a 2D list
    map_grid = [
        ['W' if random.random() < WALL_PROBABILITY else
        'C' if random.random() < CAVE_PROBABILITY else
        'M' if random.random() < MOUNTAIN_PROB and ((x < 5 or x > 26) or (y < 5 or y > 26)) else
        'T' if random.random() < TREASURE_PROB  else
        '.' for y in range(COLS)]
        for x in range(ROWS)
    ]
    return map_grid

def gen_cave(x=16, y=16):
    ROWS, COLS = x, y
    WALL_PROBABILITY = 0.2
    CAVE_PROBABILITY = 0.001
    MOUNTAIN_PROB = 0
    TREASURE_PROB = 0.001

    # Generate the map as a 2D list

    map_grid = [
        [
            val
            for tile in [
                'W' if random.random() < WALL_PROBABILITY else
                'C' if random.random() < CAVE_PROBABILITY else
                'M' if random.random() < MOUNTAIN_PROB and ((x < 5 or x > 26) or (y < 5 or y > 26)) else
                'T' if random.random() < TREASURE_PROB  else
                '.' for y in range(COLS)
            ]
            for val in (tile, ' ')
        ]
        for x in range(ROWS)
    ]

    map_grid[0][0] = '@'
    return map_grid


    # Optional: save to a text file with spaces between tiles
    # with open("random_map.txt", "w") as f:
    #     for row in map_grid:
    #         f.write(' '.join(row) + '\n')

    # Optional: print the map to terminal
    # for row in map_grid:
    #     print(' '.join(row))
