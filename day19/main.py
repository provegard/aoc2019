import intcode


def scan(program):
    for x in range(0, 50):
        for y in range(0, 50):
            output = []
            inp = [x, y]
            intcode.run(program.copy(), inp, output)
            yield output[0] 

def part1():
    """
    >>> part1()
    0
    """
    program = intcode.readProgram("input")
    return sum(scan(program))

if __name__ == "__main__":
    import doctest
    doctest.testmod()