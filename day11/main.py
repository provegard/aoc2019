from functools import reduce
import itertools
import intcode

def readNumbers(name):
    with open(name) as f:
        for line in f.readlines():
            return list(map(lambda x: int(x), line.split(",")))

# Directions:
# 0 - up
# 1 - right
# 2 - down
# 3 - left
def rotate(currentDirection, turnDirection):
    delta = 1 if turnDirection == 1 else -1
    currentDirection = (currentDirection + delta) % 4
    return currentDirection

def move(xyPosition, direction):
    (x, y) = xyPosition
    if direction == 0: y -= 1
    elif direction == 1: x += 1
    elif direction == 2: y += 1
    elif direction == 3: x -= 1
    else: raise Exception("Unknown direction %d" % (direction,))
    return (x, y)

def paintAndMove(hullMap, xyPosition, currentDirection, output):
    (paint, turnDirection) = output
    hullMap[xyPosition] = paint
    newDirection = rotate(currentDirection, turnDirection)
    return (move(xyPosition, newDirection), newDirection)

def readColor(hullMap, xyPosition):
    if not (xyPosition in hullMap):
        return 0
    return hullMap[xyPosition]

def paintHull(numbers, hullMap):
    state = None
    currentDirection = 0 # up
    currentPos = (0, 0)
    while True:
        input = [readColor(hullMap, currentPos)]
        output = []
        state = intcode.run(numbers, input, output, state)
        if state[0] == True:
            break
        (currentPos, currentDirection) = paintAndMove(hullMap, currentPos, currentDirection, output)
    
def part1():
    """
    >>> part1()
    2392
    """
    numbers = readNumbers("input")
    hullMap = {}
    paintHull(numbers, hullMap)
    return len(hullMap.keys())

def renderColor(xyPosition, color, canvas):
    (x, y) = xyPosition
    # offset so that (0,0) is in the middle
    x += 50
    y += 50
    row = canvas[y]
    row[x] = "#" if color == 1 else " "

def render(hullMap):
    canvas = []
    for _ in range(0, 100):
        emptyRow = [" "] * 100
        canvas.append(emptyRow)
    for k in hullMap.keys():
        pos = k
        color = hullMap[k]
        renderColor(pos, color, canvas)
    ascii = "\n".join(map(lambda r: "".join(r), canvas))
    return ascii

def part2():
    numbers = readNumbers("input")
    hullMap = {}
    hullMap[(0, 0)] = 1 # white
    paintHull(numbers, hullMap)
    print(render(hullMap))
    
if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    part2()
