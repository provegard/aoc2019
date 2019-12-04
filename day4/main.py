
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

def valid2(a):
    """
    >>> valid2(112233)
    True
    >>> valid2(123444)
    False
    >>> valid2(111122)
    True
    >>> valid2(111112)
    False
    >>> valid2(223456)
    True
    """
    last = a % 10
    a = a // 10
    same = 0
    foundDbl = False
    while a > 0:
        current = a % 10
        if current > last:
            return False
        if current == last:
            same += 1
        elif not foundDbl:
            foundDbl = same == 1
            same = 0
        a = a // 10
        last = current
    if not foundDbl:
        foundDbl = same == 1
    return foundDbl

def test(a, b):
    count = 0
    for x in range(a, b+1):
        if valid2(x):
            count += 1
    return count


if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    print(test(347312, 805915))
