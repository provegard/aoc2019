def splitStr(s): return [ch for ch in s]

def buildGrid(lines, level):
    grid = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(splitStr(line)):
            pos = (x, y, level)
            grid[pos] = ch
    return grid

def adjacent(pos):
    x, y, level = pos
    return [(x - 1, y, level), (x + 1, y, level), (x, y - 1, level), (x, y + 1, level)]

def adjacentRecursive(pos):
    x, y, level = pos
    naive = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    ret = []
    for px, py in naive:
        if px == 2 and py == 2:
            # adjacent square is the middle square, so expand and increase level
            if x == 1:
                # entire left side of inner grid
                newOnes = [(0, yy, level + 1) for yy in range(0, 5)]
            elif x == 3:
                # entire right side of inner grid
                newOnes = [(4, yy, level + 1) for yy in range(0, 5)]
            elif y == 1:
                # entire top side of inner grid
                newOnes = [(xx, 0, level + 1) for xx in range(0, 5)]
            elif y == 3:
                # entire bottom side of inner grid
                newOnes = [(xx, 4, level + 1) for xx in range(0, 5)]
            for no in newOnes:
                ret.append(no)
        elif px < 0:
            # adjacent square is to the left of the grid, identify square and decrease level
            ret.append((1, 2, level - 1))
        elif py < 0:
            # adjacent square is above the grid, identify square and decrease level
            ret.append((2, 1, level - 1))
        elif px > 4:
            # adjacent square is to the right of the grid, identify square and decrease level
            ret.append((3, 2, level - 1))
        elif py > 4:
            # adjacent square is below the grid, identify square and decrease level
            ret.append((2, 3, level - 1))
        else:
            # square on the same level
            ret.append((px, py, level))
    return ret


BUG = "#"
EMPTY = "."

def countAdjacentBugs(grid, pos):
    adj = adjacent(pos)
    chs = [grid.get(a, EMPTY) for a in adj]
    return len(list(filter(lambda ch:ch==BUG, chs)))

def countBugs(grid, positions):
    chs = [grid.get(a, EMPTY) for a in positions]
    return len(list(filter(lambda ch:ch==BUG, chs)))

def transform(grid):
    nxt = {}
    for pos, ch in grid.items():
        cnt = countAdjacentBugs(grid, pos)
        if ch == BUG:
            nch = BUG if cnt == 1 else EMPTY
        else:
            nch = BUG if cnt == 1 or cnt == 2 else EMPTY
        nxt[pos] = nch
    return nxt

def newBugState(ch, cnt):
    if ch == BUG:
        nch = BUG if cnt == 1 else EMPTY
    else:
        nch = BUG if cnt == 1 or cnt == 2 else EMPTY
    return nch
def transformRecursive(grid):
    nxt = {}
    positionsToConsider = set(grid.keys())
    # add in all adjacent
    for pos in positionsToConsider.copy():
        adj = adjacentRecursive(pos)
        for a in adj:
            positionsToConsider.add(a)

    for pos in positionsToConsider:
        adj = adjacentRecursive(pos)
        ch = grid.get(pos, EMPTY)
        cnt = countBugs(grid, adj)
        nch = newBugState(ch, cnt)
        nxt[pos] = nch
    return nxt

def biodiversity(grid):
    s = 0
    for pos, ch in grid.items():
        x, y, _ = pos
        power = y * 5 + x
        value = 2 ** power
        if ch == BUG:
            s += value
    return s

INPUT = [
    "#..#.",
    ".....",
    ".#..#",
    ".....",
    "#.#.."
]

def part1():
    grid = buildGrid(INPUT, 1)
    seen = [grid]
    while True:
        grid = transform(grid)
        if grid in seen:
            print(biodiversity(grid))
            return
        seen.append(grid)

def p2(lines, cutoff):
    grid = buildGrid(lines, 1)
    del grid[(2, 2, 1)]
    minutes = 0
    while minutes < cutoff:
        grid = transformRecursive(grid)
        minutes += 1
    print(countBugs(grid, grid.keys()))

def p2test():
    lines = [
        "....#",
        "#..#.",
        "#..##",
        "..#..",
        "#...."
    ]
    p2(lines, 10)

def part2():
    p2(INPUT, 200)


if __name__ == "__main__":
    #part1() # 32526865
    #p2test()
    part2() # 2009