import intcode
import os

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
MOVED = 1
OXYSYS = 2

def inverseDirection(direction):
    if direction == NORTH: return SOUTH
    if direction == SOUTH: return NORTH
    if direction == EAST: return WEST
    return EAST

def updatePos(pos, direction):
    (x, y) = pos
    if direction == NORTH: return (x, y-1)
    if direction == SOUTH: return (x, y+1)
    if direction == EAST: return (x+1, y)
    return (x-1, y)

def render(theMap, currentPos):
    os.system("cls")
    positions = theMap.keys()
    xs = list(map(lambda k:k[0], positions))
    ys = list(map(lambda k:k[1], positions))
    minX = min(xs)
    maxX = max(xs)
    minY = min(ys)
    maxY = max(ys)
    for y in range(minY, maxY+1):
        row = ""
        for x in range(minX, maxX+1):
            pos = (x, y)
            cell = " "
            if currentPos == pos:
                cell = "D"
            elif pos in theMap:
                cell = theMap[pos]
            row += cell
        print(row)
    print("pos = %s" % (currentPos, ))

def explore(pos, runner, steps, theMap, cameFrom = None):
    #visited.add(pos)
    theMap[pos] = "."
    render(theMap, pos)
    for direction in [NORTH, EAST, SOUTH, WEST]:
        if direction == cameFrom:
            # don't explore back
            continue
        newPos = updatePos(pos, direction)
        if newPos in theMap:
            # don't explore a known position
            continue
        result = runner(direction)
        if result == OXYSYS:
            # hit the goal
            theMap[newPos] = "X"
            render(theMap, pos)
            return steps + 1
        elif result == MOVED:
            # could move
            newCameFrom = inverseDirection(direction)
            ret = explore(newPos, runner, steps + 1, theMap, newCameFrom)
            if not (ret is None):
                return ret
            xx = runner(newCameFrom) # move back
            if xx != MOVED:
                raise Exception("Expected MOVED from move-back")
        else:
            # hit wall, didn't move
            theMap[newPos] = "#"
    render(theMap, pos)
    return None

# 218
def part1():
    program = intcode.readProgram("input")
    stateContainer = { "state": None }
    def runner(direction):
        output = []
        state = stateContainer["state"]
        state = intcode.run(program, [direction], output, state)
        stateContainer["state"] = state
        return output[0]
    return explore((0, 0), runner, 0, {})

if __name__ == "__main__":
    steps = part1()
    print(steps)