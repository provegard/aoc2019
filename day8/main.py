from itertools import dropwhile

def readInput():
    with open("input") as f:
        for line in f.readlines():
            return line

def chunks(iterable, n):
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]

def toLayers(digits, width, height):
    return chunks(digits, width * height)

def countDigitsOnLayer(layer, digit):
    return len(list(filter(lambda d: d == digit, layer)))

def calcPixel(tup):
    """
    >>> calcPixel(('2', '0'))
    '0'
    >>> calcPixel(('2', '2', '1'))
    '1'
    >>> calcPixel(('2', '2'))
    '2'
    """
    rest = list(dropwhile(lambda d: d == '2', tup))
    return rest[0] if len(rest) > 0 else '2'

def stack(layers):
    tuples = zip(*layers)
    return list(map(lambda t: calcPixel(t), tuples))

def renderPixel(px):
    if px == '2': return ' '
    if px == '1': return '#'
    if px == '0': return '.'
    raise Exception("Unknown: %s" % (px, ))

def renderRow(row):
    return "".join(list(map(renderPixel, row)))

def render(image, width, height):
    if len(image) % (width * height) != 0:
        raise Exception("Unexpected image length")
    rows = chunks(image, width)
    return "\n".join(list(map(renderRow, rows)))

def part1():
    """
    >>> part1()
    2016
    """
    digits = readInput()
    layers = toLayers(digits, 25, 6)
    layerWithFewest0 = min(layers, key=lambda l: countDigitsOnLayer(l, '0'))
    numberOf1 = countDigitsOnLayer(layerWithFewest0, '1')
    numberOf2 = countDigitsOnLayer(layerWithFewest0, '2')
    return numberOf1 * numberOf2

def part2():
    digits = readInput()
    layers = toLayers(digits, 25, 6)
    stacked = stack(layers)
    return render(stacked, 25, 6)

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    print(part2())
