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

    #def copy(self): return Moon(self.x, self.y, self.z, self.v)

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

def calcTotal(moons, steps):
    runSteps(moons, steps)
    totals = map(lambda m: m.totalEnergy(), moons)
    return sum(totals)

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
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
