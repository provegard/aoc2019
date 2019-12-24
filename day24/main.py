def splitStr(s): return [ch for ch in s]

def buildGrid(lines):
    grid = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(splitStr(line)):
            pos = (x, y)
            grid[pos] = ch
    return grid

def adjacent(pos):
    x, y = pos
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

BUG = "#"
EMPTY = "."

def countAdjacentBugs(grid, pos):
    adj = adjacent(pos)
    chs = [grid.get(a, EMPTY) for a in adj]
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

def biodiversity(grid):
    s = 0
    for pos, ch in grid.items():
        x, y = pos
        power = y * 5 + x
        value = 2 ** power
        if ch == BUG:
            s += value
    return s


def part1():
    lines = [
        "#..#.",
        ".....",
        ".#..#",
        ".....",
        "#.#.."
    ]
    grid = buildGrid(lines)
    seen = [grid]
    while True:
        grid = transform(grid)
        if grid in seen:
            print(biodiversity(grid))
            return
        seen.append(grid)



if __name__ == "__main__":
    part1() # 32526865