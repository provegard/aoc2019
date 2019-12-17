import intcode

def draw(output):
    chars = list(map(chr, output))
    print("".join(chars))

def valueAt(coords, pos):
    if not (pos in coords):
        return " "
    return coords[pos]

def isIntersection(coords, pos):
    (x, y) = pos
    return valueAt(coords, pos) == 35 and \
        valueAt(coords, (x-1, y)) == 35 and \
        valueAt(coords, (x+1, y)) == 35 and \
        valueAt(coords, (x, y-1)) == 35 and \
        valueAt(coords, (x, y+1)) == 35

def toCoords(output):
    y = 0
    x = 0
    coords = {}
    for charCode in output:
        coords[(x, y)] = charCode
        if charCode == 10:
            y += 1
            x = -1
        x += 1
    return coords

def part1():
    program = intcode.readProgram("input")
    output = []
    intcode.run(program, [], output)
    coords = toCoords(output)
    intersectionPoints = filter(lambda p:isIntersection(coords, p), coords.keys())

    #width = output.index(10)
    #for p in intersectionPoints:
    #    (x, y) = p
    #    idx = (width+1)*y + x
    #    output[idx] = ord("O")
    #draw(output)

    return sum(map(lambda p: p[0]*p[1], intersectionPoints))
    #draw(output)

if __name__ == "__main__":
    # 9102 wrong
    print(part1())
    #import doctest
    #doctest.testmod()