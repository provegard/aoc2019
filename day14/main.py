from typing import List
from dataclasses import dataclass
import math
import itertools

@dataclass
class Amount:
    qty: int
    chemical: str

    def requireSameChemical(self, other):
        if self.chemical != other.chemical:
            raise Exception("error %s vs %s" % (self.chemical, other.chemical))

    def mul(self, n):
        return Amount(self.qty * n, self.chemical)

    def withQty(self, qty):
        return Amount(qty, self.chemical)

    def reducedBy(self, other):
        self.requireSameChemical(other)
        if other.qty > self.qty:
            newMe = self.withQty(0)
            newOther = other.withQty(other.qty - self.qty)
            return (newMe, newOther)
        newMe = self.withQty(self.qty - other.qty)
        newOther = other.withQty(0)
        return (newMe, newOther)

    def sameChemicalAs(self, other):
        return self.chemical == other.chemical

@dataclass
class Reaction:
    inputs: List[Amount]
    output: Amount

    def outputChemical(self): return self.output.chemical

    def runCount(self, goal: Amount):
        output = self.output
        output.requireSameChemical(goal)
        return math.ceil(goal.qty / output.qty)

    def onlyNeedsOre(self):
        return len(self.inputs) == 1 and self.inputs[0].chemical == "ORE"

FuelGoel = Amount(1, "FUEL")

def parseAmount(s):
    [qty, chem] = s.split(" ")
    return Amount(int(qty), chem.strip())

def parseReaction(line):
    """
    >>> parseReaction("10 ORE => 10 A")
    Reaction(inputs=[Amount(qty=10, chemical='ORE')], output=Amount(qty=10, chemical='A'))
    >>> parseReaction("7 A, 1 B => 1 C")
    Reaction(inputs=[Amount(qty=7, chemical='A'), Amount(qty=1, chemical='B')], output=Amount(qty=1, chemical='C'))
    """
    [i, o] = line.split(" => ")
    amounts = i.split(", ")
    inputs = list(map(parseAmount, amounts))
    output = parseAmount(o)
    return Reaction(inputs, output)

def readReactions(name):
    with open(name) as f:
        for line in f.readlines():
            yield parseReaction(line)

def buildTree(reactions):
    tree = {}
    for r in reactions:
        # assume there's only one for now
        if r.outputChemical() in tree:
            raise Exception("there are many :(")
        tree[r.outputChemical()] = r
    return tree

def reduce(needs):
    """
    >>> reduce([Amount(1, "A")])
    [Amount(qty=1, chemical='A')]
    >>> reduce([Amount(1, "A"), Amount(2, "A")])
    [Amount(qty=3, chemical='A')]
    >>> reduce([Amount(1, "B"), Amount(2, "A")])
    [Amount(qty=2, chemical='A'), Amount(qty=1, chemical='B')]
    >>> reduce([Amount(0, "A")])
    []
    """
    sortedNeeds = sorted(needs, key=lambda a:a.chemical)
    groups = itertools.groupby(sortedNeeds, key=lambda a:a.chemical)
    result = []
    for (chem, amounts) in groups:
        qtys = map(lambda a:a.qty, amounts)
        newQty = sum(qtys)
        if newQty > 0:
            result.append(Amount(newQty, chem))
    return result

def useSurplus(n, surplus):
    ns = []
    for s in surplus:
        if s.sameChemicalAs(n):
            (n, ss) = n.reducedBy(s)
            ns.append(ss)
        else:
            ns.append(s) # still a surplus
    return (n, ns)

def satisfy(reactionTree, needs: List[Amount], surplus: List[Amount]):
    newNeeds = []
    for n in needs:
        (n, surplus) = useSurplus(n, surplus)

        reaction = reactionTree[n.chemical]
        if reaction.onlyNeedsOre():
            # let this need stay, we'll calc ORE later
            newNeeds.append(n)
            continue
        cnt = reaction.runCount(n)

        if cnt > 0:
            # figure out surplus
            produced = reaction.output.mul(cnt)
            (_, extra) = n.reducedBy(produced)
            surplus.append(extra)

            # new needs based on inputs
            for inp in reaction.inputs:
                newNeeds.append(inp.mul(cnt))

    ret = reduce(newNeeds)
    if ret == needs:
        # Figure out ORE need
        finalNeeds = []
        for n in ret:
            reaction = reactionTree[n.chemical]
            cnt = reaction.runCount(n)
            for inp in reaction.inputs:
                finalNeeds.append(inp.mul(cnt))
        finalNeeds = reduce(finalNeeds)
        return (True, finalNeeds, [])
    ns = reduce(surplus)
    return (False, ret, ns)

def naive(reactionTree, goal: Amount):
    needs = [goal]
    surplus = []
    done = False
    while not done:
        (done, needs, surplus) = satisfy(reactionTree, needs, surplus)
    if len(needs) != 1 or needs[0].chemical != "ORE":
        raise Exception("Unexpected: %s" % (needs, ))
    return needs[0].qty

def buildReactionTree(name):
    reactions = list(readReactions(name))
    return buildTree(reactions)

def example(fn):
    """
    >>> example("example1")
    31
    >>> example("example2")
    165
    >>> example("example3")
    13312
    >>> example("example4")
    180697
    >>> example("example5")
    2210736
    """
    rt = buildReactionTree(fn)
    return naive(rt, FuelGoel)

def example2(fn):
    """
    >>> example2("example3")
    82892753
    >>> example2("example4")
    5586022
    >>> example2("example5")
    460664
    """
    rt = buildReactionTree(fn)
    #n = 1000
    lastN = 1
    n = 1
    delta = 100000
    while True:
        ore = naive(rt, Amount(n, "FUEL"))
        if ore > 1000000000000:
            if delta == 1:
                return n - 1
            # went too far, backtrack and reduce delta
            delta = delta // 2
            n = lastN
        lastN = n
        n = lastN + delta
    return -1


# 414725 too high
# 141665 too low
def part1():
    """
    >>> part1()
    387001
    """
    return example("input")

def part2():
    """
    >>> part2()
    3412429
    """
    return example2("input")

if __name__ == "__main__":
    import doctest
    doctest.testmod()