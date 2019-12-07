from functools import reduce
import itertools

def readNumbers(name):
    with open(name) as f:
        for line in f.readlines():
            return list(map(lambda x: int(x), line.split(",")))

def update(lst, pos, value):
    # never in immediate mode
    idx = lst[pos]
    lst[idx] = value
def get(lst, pos, modes):
    mode = 0
    if len(modes) > 0:
        mode = modes.pop(0)
    if mode == 0:
        # position mode
        return lst[lst[pos]]
    # immediate mode
    return lst[pos]

def decodeInstruction(ins):
    """
    >>> decodeInstruction(1002)
    (2, [0, 1])
    """
    opcode = ins % 100
    modes = ins // 100
    modeArr = []
    while modes > 0:
        modeArr.append(modes % 10)
        modes = modes // 10
    return (opcode, modeArr)

def getInput(inputs):
    if len(inputs) == 0:
        raise Exception("No more inputs")
    return inputs.pop(0)

def run(numbers, inputs, output):
    """
    >>> run([1,0,0,0,99], [1], [])
    [2, 0, 0, 0, 99]
    >>> run([2,3,0,3,99], [1], [])
    [2, 3, 0, 6, 99]
    >>> run([2,4,4,5,99,0], [1], [])
    [2, 4, 4, 5, 99, 9801]
    >>> run([1,1,1,4,99,5,6,0,99], [1], [])
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    >>> run([3,0,4,0,99], [1], [])
    [1, 0, 4, 0, 99]
    >>> run([1101,100,-1,4,0], [1], [])
    [1101, 100, -1, 4, 99]
    """
    pos = 0
    while True:
        ins = numbers[pos]
        (opcode, modes) = decodeInstruction(ins)
        if opcode == 1:
            t1 = get(numbers, pos + 1, modes)
            t2 = get(numbers, pos + 2, modes)
            update(numbers, pos + 3, t1 + t2)
            pos += 4
        elif opcode == 2:
            t1 = get(numbers, pos + 1, modes)
            t2 = get(numbers, pos + 2, modes)
            update(numbers, pos + 3, t1 * t2)
            pos += 4
        elif opcode == 3:
            update(numbers, pos + 1, getInput(inputs))
            pos += 2
        elif opcode == 4:
            value = get(numbers, pos + 1, modes)
            output.append(value)
            pos += 2
        elif opcode == 5:
            # jump-if-true
            first = get(numbers, pos + 1, modes)
            second = get(numbers, pos + 2, modes)
            if first != 0:
                pos = second
            else:
                pos += 3
        elif opcode == 6:
            # jump-if-false
            first = get(numbers, pos + 1, modes)
            second = get(numbers, pos + 2, modes)
            if first == 0:
                pos = second
            else:
                pos += 3
        elif opcode == 7:
            # less-than
            first = get(numbers, pos + 1, modes)
            second = get(numbers, pos + 2, modes)
            if first < second:
                update(numbers, pos + 3, 1)
            else:
                update(numbers, pos + 3, 0)
            pos += 4
        elif opcode == 8:
            # equals
            first = get(numbers, pos + 1, modes)
            second = get(numbers, pos + 2, modes)
            if first == second:
                update(numbers, pos + 3, 1)
            else:
                update(numbers, pos + 3, 0)
            pos += 4
        elif opcode == 99:
            return numbers
        else:
            raise Exception("Unknown opcode %d" % (opcode,))

def runSequence(numbers, sequence):
    """
    >>> runSequence([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0])
    43210
    >>> runSequence([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4])
    54321
    >>> runSequence([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2])
    65210
    """
    currentInput = 0
    for s in sequence:
        nums = numbers.copy()
        output = []
        run(nums, [s, currentInput], output)
        currentInput = output[-1]

    return currentInput


def part1():
    """
    >>> part1()
    0
    """
    numbers = readNumbers("input")
    possible = [0, 1, 2, 3, 4]
    results = []
    for x in list(itertools.permutations(possible)):
        results.append(runSequence(numbers, x))
    return max(results)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
