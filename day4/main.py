
import math
import re
import typing

def valid(a):
    """
    >>> valid(111111)
    True
    >>> valid(223450)
    False
    >>> valid(123789)
    False
    """
    last = a % 10
    a = a // 10
    foundDbl = False
    while a > 0:
        current = a % 10
        if current > last:
            return False
        if current == last:
            foundDbl = True
        a = a // 10
        last = current
    return foundDbl


def test(a, b):
    count = 0
    for x in range(a, b+1):
        if valid(x):
            count += 1
    return count


# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
if __name__ == "__main__":
    print(test(347312, 805915))
