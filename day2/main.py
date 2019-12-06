
def readNumbers():
    with open("input") as f:
        for line in f.readlines():
            return list(map(lambda x: int(x), line.split(",")))

def listSet(lst, idx, value):
    lst[idx] = value

def run(numbers):
    """
    >>> run([1,0,0,0,99])
    [2, 0, 0, 0, 99]
    >>> run([2,3,0,3,99])
    [2, 3, 0, 6, 99]
    >>> run([2,4,4,5,99,0])
    [2, 4, 4, 5, 99, 9801]
    >>> run([1,1,1,4,99,5,6,0,99])
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    """
    pos = 0
    while True:
        opcode = numbers[pos]
        if opcode == 1:
            t1 = numbers[numbers[pos+1]]
            t2 = numbers[numbers[pos+2]]
            dest = numbers[pos+3]
            listSet(numbers, dest, t1 + t2)
        elif opcode == 2:
            t1 = numbers[numbers[pos+1]]
            t2 = numbers[numbers[pos+2]]
            dest = numbers[pos+3]
            listSet(numbers, dest, t1 * t2)
        elif opcode == 99:
            return numbers
        else:
            raise Exception("Unknown opcode %d" % (opcode,))
        pos += 4

def findNounVerb(numbers, target):
    for noun in range(0, 99):
        for verb in range(0, 99):
            newnums = numbers.copy()
            newnums[1] = noun
            newnums[2] = verb
            run(newnums)
            if newnums[0] == target:
                return (noun, verb)
    raise Exception("Nothing found")

def part1():
    """
    >>> part1()
    3654868
    """
    nums = readNumbers()
    nums[1] = 12
    nums[2] = 2
    run(nums)
    return nums[0]

def part2():
    """
    >>> part2()
    7014
    """
    nums = readNumbers()
    tup = findNounVerb(nums, 19690720)
    return tup[0] * 100 + tup[1]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
