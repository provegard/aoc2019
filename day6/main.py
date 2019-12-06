

def readInput(name):
    with open(name) as f:
        return f.readlines()

def decodeOrbit(orbit):
    return orbit.strip().split(")")

def buildOrbitMap(orbits):
    res = {}
    for orbit in orbits:
        parts = decodeOrbit(orbit)
        # AAA)BBB = BBB orbits AAA, so we put BBB -> AAA
        res[parts[1]] = parts[0]
    return res

def countOrbitsFor(orbitMap, obj):
    if obj == "COM":
        return 0
    target = orbitMap[obj]
    return 1 + countOrbitsFor(orbitMap, target)

def countOrbits(orbitMap):
    s = 0
    for k in orbitMap.keys():
        s += countOrbitsFor(orbitMap, k)
    return s

def example():
    """
    >>> example()
    42
    """
    orbits = readInput("test_input")
    orbitMap = buildOrbitMap(orbits)
    return countOrbits(orbitMap)

def part1():
    """
    >>> part1()
    0
    """
    orbits = readInput("input")
    orbitMap = buildOrbitMap(orbits)
    return countOrbits(orbitMap)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
