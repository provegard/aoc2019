
import re
import typing

def lmap(func, *iterables):
    return list(map(func, *iterables))
def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))
def fileLines(filename):
    with open("input") as f:
        return f.readlines()
