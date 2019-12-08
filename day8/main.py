def readInput():
    with open("input") as f:
        for line in f.readlines():
            return line

def toLayers(digits, width, height):
    n = width * height
    return [digits[i:i+n] for i in range(0, len(digits), n)]

def countDigitsOnLayer(layer, digit):
    return len(list(filter(lambda d: d == digit, layer)))

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
