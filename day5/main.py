
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
    """
    pos = 0
    while True:
        opcode = numbers[pos]
        if opcode == 1:
            t1 = ref(numbers, pos + 1)
            t2 = ref(numbers, pos + 2)
            update(numbers, pos + 3, t1 + t2)
            pos += 4
        elif opcode == 2:
            t1 = ref(numbers, pos + 1)
            t2 = ref(numbers, pos + 2)
            update(numbers, pos + 3, t1 * t2)
            pos += 4
        elif opcode == 3:
            update(numbers, pos + 1, input)
            pos += 2
        elif opcode == 4:
            value = ref(numbers, pos + 1)
            output.append(value)
            pos += 2
        elif opcode == 99:
            return numbers
        else:
            raise Exception("Unknown opcode %d" % (opcode,))

def test1(numbers):
    """
    >>> test1([3,0,4,0,99])
    [77]
    """
    output = []
    run(numbers, 77, output)
    return output


if __name__ == "__main__":
    import doctest
    doctest.testmod()
