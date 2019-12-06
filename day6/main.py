from functools import reduce

def readInput(name):
    with open(name) as f:
        return f.readlines()

def decodeOrbit(orbit):
    parts = orbit.strip().split(")")
    return (parts[0], parts[1])

def buildOrbitMap(orbits):
    res = {}
    for orbit in orbits:
        (around, orbiting) = decodeOrbit(orbit)
        # AAA)BBB = BBB orbits AAA, so we put BBB -> AAA
        res[orbiting] = around
    return res

def countOrbitsFor(orbitMap, obj):
    return 0 if obj == "COM" else 1 + countOrbitsFor(orbitMap, orbitMap[obj])

def countOrbits(orbitMap):
    return reduce(lambda acc, k: acc + countOrbitsFor(orbitMap, k), orbitMap.keys(), 0)

def count(f):
    orbits = readInput(f)
    orbitMap = buildOrbitMap(orbits)
    return countOrbits(orbitMap)

def pathFromCOM(orbitMap, obj):
    return ["COM"] if obj == "COM" else pathFromCOM(orbitMap, orbitMap[obj]) + [obj]


def stripCommonPrefix(a, b):
    while a[0] == b[0]:
        a.pop(0)
        b.pop(0)

def countSteps(orbitMap, src, dst):
    p1 = pathFromCOM(orbitMap, src)
    p2 = pathFromCOM(orbitMap, dst)
    stripCommonPrefix(p1, p2)
    return len(p1) + len(p2) - 2
    
def steps(f):
    orbits = readInput(f)
    orbitMap = buildOrbitMap(orbits)
    return countSteps(orbitMap, "YOU", "SAN")

def example():
    """
    >>> example()
    42
    """
    return count("test_input")

def part1():
    """
    >>> part1()
    151345
    """
    return count("input")
    
def example2():
    """
    >>> example2()
    4
    """
    return steps("test_input_2")
    
def part2():
    """
    >>> part2()
    391
    """
    return steps("input")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
