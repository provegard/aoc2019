
def split(word): 
    return [int(char) for char in word]

def sumsForElemNo(inputList, n):
    for idx in range(n-1, len(inputList), 4*n):
        yield sum(inputList[idx:idx+n])
        yield -sum(inputList[2*n+idx:3*n+idx])

def processOneGen(inputList):
    for idx in range(0, len(inputList)):
        n = idx + 1
        s = sum(sumsForElemNo(inputList, n))
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
    return "".join(map(str, inputList))[:8]

# def process2(numbers, phases):
#     """
#     >>> process2("03036732577212944063491565474664", 100)
#     '84462026'
#     """
#     offset = int(numbers[0:7])
#     inputList = split(numbers) * 10000
#     for _ in range(0, phases):
#         inputList = list(processOneGen(inputList))
#     resultStr = "".join(map(str, inputList))
#     return resultStr[offset:offset+8]


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
