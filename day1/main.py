
import math
from functools import reduce

def readMasses():
    with open("input") as f:
        return list(map(lambda x: int(x), f.readlines()))

def fuel(mass):
    return math.floor(mass / 3) - 2

def fuelRec(f):
    if f <= 0:
        return 0
    f2 = fuel(f)
    return f + fuelRec(f2)

def main(recurse):
    fuels = map(fuel, readMasses())
    return reduce(lambda acc, f: acc + fuelRec(f), fuels, 0) if recurse else sum(fuels)

def part1():
    """
    >>> part1()
    3249140
    """
    return main(False)

def part2():
    """
    >>> part2()
    4870838
    """
    return main(True)

if __name__ == "__main__":
    import doctest
    doctest.testmod()