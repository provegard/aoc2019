from functools import reduce
import itertools
import os
import time

import intcode

def readNumbers(name):
    with open(name) as f:
        for line in f.readlines():
            return list(map(lambda x: int(x), line.split(",")))

def renderTile(xyPosition, tile_id, canvas):
    (x, y) = xyPosition
    row = canvas[y]
    tile = " "
    if tile_id == WALL:   tile = "|"
    if tile_id == BLOCK:  tile = "#"
    if tile_id == PADDLE: tile = "="
    if tile_id == BALL:   tile = "o"
    row[x] = tile

def render(grid, w, h):
    canvas = []
    for _ in range(0, h):
        emptyRow = [" "] * w
        canvas.append(emptyRow)
    for k in grid.keys():
        pos = k
        tile_id = grid[k]
        renderTile(pos, tile_id, canvas)
    ascii = "\n".join(map(lambda r: "".join(r), canvas))
    return ascii

def measure(grid):
    w = 0
    h = 0
    for (x, y) in grid.keys():
        w = max(w, x)
        h = max(h, y)
    return (w + 1, h + 1)

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

FREE_PLAY = 2

def display(grid):
    (width, height) = measure(grid)
    os.system("cls")
    print(render(grid, width, height))
    #time.sleep(0.5)

def markTiles(grid, output, scoreList):
    for i in range(0, len(output), 3):
        [x, y, tile_id] = output[i:i+3]
        if x == -1 and y == 0:
            scoreList[0] = tile_id
        else:
            grid[(x, y)] = tile_id

def runGame(numbers, grid):
    output = []
    state = intcode.run(numbers, [], output, None)
    if state[0] != True:
        raise Exception("input needed??")
    markTiles(grid, output, [])

def findPos(grid, tile_id):
    for k in grid.keys():
        if grid[k] == tile_id:
            return k
    raise Exception("not found %d" % (tile_id,))

def playGame(numbers, grid):
    scoreList = [0]
    inp = []
    state = None
    while True:
        output = []
        state = intcode.run(numbers, inp, output, state)
        markTiles(grid, output, scoreList)
        #display(grid)
        #print("SCORE = %d" % (scoreList[0],))
        if state[0] != True:
            (px, _) = findPos(grid, PADDLE)
            (bx, _) = findPos(grid, BALL)
            move = 0
            if bx < px: move = -1
            elif bx > px: move = 1
            inp = [move]
        else:
            return scoreList[0]
    
def part1():
    """
    >>> part1()
    180
    """
    numbers = readNumbers("input")
    grid = {}
    runGame(numbers, grid)
    return len(list(filter(lambda x:x == BLOCK, grid.values())))

def part2():
    numbers = readNumbers("input")
    numbers[0] = FREE_PLAY
    grid = {}
    score = playGame(numbers, grid)
    print(score)
    
if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    part2()