
BasePattern = [0, 1, 0, -1]

def split(word): 
    return [int(char) for char in word]

def patternForElemNo(n):
    first = True
    while True:
        # for each pattern value
        for d in BasePattern:
            # repeat N times
            for _ in range(0, n):
                # skip the first!
                if not first:
                    yield d
                first = False

def processOneGen(inputList):
    for idx in range(0, len(inputList)):
        elemNo = idx + 1
        s = 0
        for t in zip(inputList, patternForElemNo(elemNo)):
            s += t[0] * t [1]
        yield abs(s) % 10

def process(number, phases):
    """
    >>> process("12345678", 1)
    '48226158'
    >>> process("12345678", 2)
    '34040438'
    >>> process("12345678", 4)
    '01029498'
    >>> process("80871224585914546619083218645595", 100)
    '24176176'
    """
    inputList = split(number)
    for _ in range(0, phases):
        inputList = list(processOneGen(inputList))
    #return "".join(inputList)
    return "".join(map(str, inputList))[:8]


def readInput():
    with open("input") as f:
        return f.readlines()[0]

def part1():
    """
    >>> part1()
    '78009100'
    """
    return process(readInput(), 100)

def part2():
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
