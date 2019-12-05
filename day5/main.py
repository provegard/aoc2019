
import math

def readNumbers():
    with open("input") as f:
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

def run(numbers, input, output):
    """
    >>> run([1,0,0,0,99], 1, [])
    [2, 0, 0, 0, 99]
    >>> run([2,3,0,3,99], 1, [])
    [2, 3, 0, 6, 99]
    >>> run([2,4,4,5,99,0], 1, [])
    [2, 4, 4, 5, 99, 9801]
    >>> run([1,1,1,4,99,5,6,0,99], 1, [])
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    >>> run([3,0,4,0,99], 1, [])
    [1, 0, 4, 0, 99]
    >>> run([1101,100,-1,4,0], 1, [])
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
            update(numbers, pos + 1, input)
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

def test1(numbers, input):
    """
    >>> test1([3,9,8,9,10,9,4,9,99,-1,8], 8)
    1
    >>> test1([3,9,8,9,10,9,4,9,99,-1,8], 9)
    0
    >>> test1([3,9,7,9,10,9,4,9,99,-1,8], 7)
    1
    >>> test1([3,9,7,9,10,9,4,9,99,-1,8], 8)
    0
    >>> test1([3,3,1108,-1,8,3,4,3,99], 8)
    1
    >>> test1([3,3,1108,-1,8,3,4,3,99], 88)
    0
    >>> test1([3,3,1107,-1,8,3,4,3,99], 6)
    1
    >>> test1([3,3,1107,-1,8,3,4,3,99], 9)
    0
    >>> test1([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0)
    0
    >>> test1([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 2)
    1
    >>> test1([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 7)
    999
    >>> test1([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8)
    1000
    >>> test1([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 9)
    1001
    """
    output = []
    run(numbers, input, output)
    return output[-1]

def part1():
    """
    >>> part1()
    14522484
    """
    output = []
    numbers = readNumbers()
    run(numbers, 1, output)
    return output[-1] # last value

def part2():
    """
    >>> part2()
    0
    """
    output = []
    numbers = readNumbers()
    run(numbers, 5, output)
    return output[-1] # last value

if __name__ == "__main__":
    import doctest
    doctest.testmod()
