
def split(word): 
    return [int(char) for char in word]

def mulForElemNo(inputList, n):
    # skip (n-1) items
    idx = n - 1
    while idx < len(inputList):
        # take n
        for d in inputList[idx:idx+n]:
            yield d
        idx += n
        # skip n
        idx += n
        # then take n
        for d in inputList[idx:idx+n]:
            yield -d # yes, negative
        idx += n
        # then skip n (the first skip is outside the loop)
        idx += n

def processOneGen(inputList):
    for idx in range(0, len(inputList)):
        n = idx + 1
        s = sum(mulForElemNo(inputList, n))
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
#     inputList = inputList[offset:]
#     for _ in range(0, phases):
#         inputList = list(processOneGen(inputList, offset))
#     resultStr = "".join(map(str, inputList))
#     return resultStr[:8]
#     #return resultStr[offset:offset+8]


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
