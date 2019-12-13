from functools import reduce
import itertools

def readNumbers(name):
    with open(name) as f:
        for line in f.readlines():
            return list(map(lambda x: int(x), line.split(",")))

def setValue(lst, pos, value):
    while pos >= len(lst):
        lst.append(0)
    lst[pos] = value

def nextMode(modes):
    mode = 0
    if len(modes) > 0:
        mode = modes.pop(0)
    return mode

def update(lst, pos, value, modes, relBase):
    idx = 0
    mode = nextMode(modes)
    if mode == 2:
        # relative mode
        rel = getValueAt(lst, pos)
        idx = relBase + rel
    else:
        # position mode
        idx = getValueAt(lst, pos)
    setValue(lst, idx, value)

def getValueAt(lst, pos):
    if pos >= len(lst):
        return 0
    return lst[pos]

def get(lst, pos, modes, relBase):
    mode = nextMode(modes)
    if mode == 0:
        # position mode
        return getValueAt(lst, getValueAt(lst, pos))
        #return lst[lst[pos]]
    if mode == 2:
        # relative mode
        rel = getValueAt(lst, pos)
        idx = rel + relBase
        return getValueAt(lst, idx)
    # immediate mode
    #return lst[pos]
    return getValueAt(lst, pos)

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

def run(numbers, inputs, output, state = None):
    # """
    # >>> run([1,0,0,0,99], [1], [])
    # [2, 0, 0, 0, 99]
    # >>> run([2,3,0,3,99], [1], [])
    # [2, 3, 0, 6, 99]
    # >>> run([2,4,4,5,99,0], [1], [])
    # [2, 4, 4, 5, 99, 9801]
    # >>> run([1,1,1,4,99,5,6,0,99], [1], [])
    # [30, 1, 1, 4, 2, 5, 6, 0, 99]
    # >>> run([3,0,4,0,99], [1], [])
    # [1, 0, 4, 0, 99]
    # >>> run([1101,100,-1,4,0], [1], [])
    # [1101, 100, -1, 4, 99]
    # >>> run([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], [1], [])
    # 109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99
    # """
    pos = 0
    relBase = 0
    if not (state is None):
        numbers = state[1]
        pos = state[2]
        relBase = state[3]
    while True:
        ins = numbers[pos]
        (opcode, modes) = decodeInstruction(ins)
        if opcode == 1:
            t1 = get(numbers, pos + 1, modes, relBase)
            t2 = get(numbers, pos + 2, modes, relBase)
            update(numbers, pos + 3, t1 + t2, modes, relBase)
            pos += 4
        elif opcode == 2:
            t1 = get(numbers, pos + 1, modes, relBase)
            t2 = get(numbers, pos + 2, modes, relBase)
            update(numbers, pos + 3, t1 * t2, modes, relBase)
            pos += 4
        elif opcode == 3:
            if len(inputs) == 0:
                return (False, numbers, pos, relBase)
                #raise Exception("no input :(")
            i = inputs.pop(0)
            update(numbers, pos + 1, i, modes, relBase)
            pos += 2
        elif opcode == 4:
            value = get(numbers, pos + 1, modes, relBase)
            output.append(value)
            pos += 2
        elif opcode == 5:
            # jump-if-true
            first = get(numbers, pos + 1, modes, relBase)
            second = get(numbers, pos + 2, modes, relBase)
            if first != 0:
                pos = second
            else:
                pos += 3
        elif opcode == 6:
            # jump-if-false
            first = get(numbers, pos + 1, modes, relBase)
            second = get(numbers, pos + 2, modes, relBase)
            if first == 0:
                pos = second
            else:
                pos += 3
        elif opcode == 7:
            # less-than
            first = get(numbers, pos + 1, modes, relBase)
            second = get(numbers, pos + 2, modes, relBase)
            valueToSet = 1 if first < second else 0
            update(numbers, pos + 3, valueToSet, modes, relBase)
            pos += 4
        elif opcode == 8:
            # equals
            first = get(numbers, pos + 1, modes, relBase)
            second = get(numbers, pos + 2, modes, relBase)
            valueToSet = 1 if first == second else 0
            update(numbers, pos + 3, valueToSet, modes, relBase)
            pos += 4
        elif opcode == 9:
            first = get(numbers, pos + 1, modes, relBase)
            relBase += first
            pos += 2
        elif opcode == 99:
            #return numbers
            return (True, numbers, pos, relBase)
        else:
            raise Exception("Unknown opcode %d" % (opcode,))

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

def runGame(numbers, grid):
    output = []
    state = run(numbers, [], output, None)
    if state[0] != True:
        raise Exception("input needed??")
    for i in range(0, len(output), 3):
        [x, y, tile_id] = output[i:i+3]
        grid[(x, y)] = tile_id
    
def part1():
    """
    >>> part1()
    0
    """
    numbers = readNumbers("input")
    grid = {}
    runGame(numbers, grid)
    return len(list(filter(lambda x:x == BLOCK, grid.values())))
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
