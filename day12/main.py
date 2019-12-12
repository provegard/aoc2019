from dataclasses import dataclass

def deltaVelocity(a, b):
    """
    >>> deltaVelocity(3, 5)
    1
    >>> deltaVelocity(5, 3)
    -1
    >>> deltaVelocity(5, 5)
    0
    """
    return 1 if a < b else (0 if a == b else -1)

@dataclass
class Moon:
    x: int
    y: int
    z: int
    x_v: int = 0
    y_v: int = 0
    z_v: int = 0

    def copy(self): return Moon(self.x, self.y, self.z, self.x_v, self.y_v, self.z_v)

    def updatePosition(self):
        self.x += self.x_v
        self.y += self.y_v
        self.z += self.z_v

    def updateVelocity(self, m2):
        self.x_v += deltaVelocity(self.x, m2.x)
        self.y_v += deltaVelocity(self.y, m2.y)
        self.z_v += deltaVelocity(self.z, m2.z)

    def potentialEnergy(self): return abs(self.x) + abs(self.y) + abs(self.z)
    def kineticEnergy(self): return abs(self.x_v) + abs(self.y_v) + abs(self.z_v)
    def totalEnergy(self): return self.potentialEnergy() * self.kineticEnergy()

def updateVelocity(moons):
    for idx, m1 in enumerate(moons):
        for m2 in moons[idx+1:]:
            m1.updateVelocity(m2)
            m2.updateVelocity(m1)

def updatePosition(moons):
    for m in moons:
        m.updatePosition()

def timeStep(moons):
    updateVelocity(moons)
    updatePosition(moons)

def runSteps(moons, steps):
    for _ in range(0, steps):
        timeStep(moons)

def runStepsGen(moons):
    while True:
        timeStep(moons)
        yield moons

def calcTotal(moons, steps):
    runSteps(moons, steps)
    totals = map(lambda m: m.totalEnergy(), moons)
    return sum(totals)

def eq(moons1, moons2, pred):
    for idx, m1 in enumerate(moons1):
        m2 = moons2[idx]
        if not pred(m1, m2):
            return False
    return True

def eqX(moons1, moons2): return eq(moons1, moons2, lambda m1, m2: m1.x == m2.x and m1.x_v == m2.x_v)
def eqY(moons1, moons2): return eq(moons1, moons2, lambda m1, m2: m1.y == m2.y and m1.y_v == m2.y_v)
def eqZ(moons1, moons2): return eq(moons1, moons2, lambda m1, m2: m1.z == m2.z and m1.z_v == m2.z_v)

def findPeriodicityFor(moons, eqFun):
    copies = list(map(lambda m: m.copy(), moons))
    steps = 0
    for newMoons in runStepsGen(moons):
        steps += 1
        if eqFun(newMoons, copies):
            return steps
        if steps > 1000000:
            raise Exception("too far")

def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    return a * b / gcd(a, b)

def findPeriodicity(moons):
    x = findPeriodicityFor(moons, lambda ms1, ms2: eqX(ms1, ms2))
    y = findPeriodicityFor(moons, lambda ms1, ms2: eqY(ms1, ms2))
    z = findPeriodicityFor(moons, lambda ms1, ms2: eqZ(ms1, ms2))
    return int(lcm(lcm(x, y), z))

def example1_repr_n(steps):
    """
    >>> example1_repr_n(1)
    [Moon(x=2, y=-1, z=1, x_v=3, y_v=-1, z_v=-1), Moon(x=3, y=-7, z=-4, x_v=1, y_v=3, z_v=3), Moon(x=1, y=-7, z=5, x_v=-3, y_v=1, z_v=-3), Moon(x=2, y=2, z=0, x_v=-1, y_v=-3, z_v=1)]
    >>> example1_repr_n(10)
    [Moon(x=2, y=1, z=-3, x_v=-3, y_v=-2, z_v=1), Moon(x=1, y=-8, z=0, x_v=-1, y_v=1, z_v=3), Moon(x=3, y=-6, z=1, x_v=3, y_v=2, z_v=-3), Moon(x=2, y=0, z=4, x_v=1, y_v=-1, z_v=-1)]
    """
    moons = [
        Moon(-1, 0, 2),
        Moon(2, -10, -7),
        Moon(4, -8, 8),
        Moon(3, 5, -1)
    ]
    runSteps(moons, steps)
    return moons

def example1_total():
    """
    >>> example1_total()
    179
    """
    moons = [
        Moon(-1, 0, 2),
        Moon(2, -10, -7),
        Moon(4, -8, 8),
        Moon(3, 5, -1)
    ]
    return calcTotal(moons, 10)

def example1_steps_return():
    """
    >>> example1_steps_return()
    2772
    """
    moons = [
        Moon(-1, 0, 2),
        Moon(2, -10, -7),
        Moon(4, -8, 8),
        Moon(3, 5, -1)
    ]
    return findPeriodicity(moons)

def example2_steps_return():
    """
    >>> example2_steps_return()
    4686774924
    """
    moons = [
        Moon(-8, -10, 0),
        Moon(5, 5, 10),
        Moon(2, -7, 3),
        Moon(9, -8, -3)
    ]
    return findPeriodicity(moons)


def part1():
    """
    >>> part1()
    9958
    """
    moons = [
        Moon(7, 10, 17),
        Moon(-2, 7, 0),
        Moon(12, 5, 12),
        Moon(5, -8, 6)
    ]
    return calcTotal(moons, 1000)

def part2():
    """
    >>> part2()
    318382803780324
    """
    moons = [
        Moon(7, 10, 17),
        Moon(-2, 7, 0),
        Moon(12, 5, 12),
        Moon(5, -8, 6)
    ]
    return findPeriodicity(moons)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
