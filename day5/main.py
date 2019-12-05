
import math

def readNumbers():
    with open("input") as f:
        for line in f.readlines():
            return list(map(lambda x: int(x), line.split(",")))

def update(lst, pos, value):
    idx = lst[pos]
    lst[idx] = value
def ref(lst, pos):
    return lst[lst[pos]]

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
            t1 = ref(numbers, pos + 1)
            t2 = ref(numbers, pos + 2)
            update(numbers, pos + 3, t1 + t2)
        elif opcode == 2:
            t1 = ref(numbers, pos + 1)
            t2 = ref(numbers, pos + 2)
            update(numbers, pos + 3, t1 * t2)
        elif opcode == 99:
            return numbers
        else:
            raise Exception("Unknown opcode %d" % (opcode,))
        pos += 4

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
