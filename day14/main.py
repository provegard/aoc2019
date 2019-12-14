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

def satisfy(reactionTree, needs: List[Amount], surplus: List[Amount]):
    newNeeds = []
    newSurplus = []
    for n in needs:
        # reduce by existing surplus
        for s in surplus:
            if s.sameChemicalAs(n):
                (n, ss) = n.reducedBy(s)
                newSurplus.append(ss)
            else:
                newSurplus.append(s) # still a surplus

        reaction = reactionTree[n.chemical]
        if reaction.onlyNeedsOre():
            # let this need stay, we'll calc ORE later
            newNeeds.append(n)
            continue
        cnt = reaction.runCount(n)

        # figure out surplus
        produced = reaction.output.mul(cnt)
        (_, extra) = n.reducedBy(produced)
        newSurplus.append(extra)

        for inp in reaction.inputs:
            newNeeds.append(inp.mul(cnt))
    ret = reduce(newNeeds)
    if ret == needs:
        # TODO: Städa upp detta
        finalNeeds = []
        for n in ret:
            reaction = reactionTree[n.chemical]
            cnt = reaction.runCount(n)
            #print("Using %d * %s to get %s" % (cnt, reaction, n))
            for inp in reaction.inputs:
                finalNeeds.append(inp.mul(cnt))
        #print("finalNeeds before reduce = %s" % (finalNeeds,))
        finalNeeds = reduce(finalNeeds)
        return (True, finalNeeds, newSurplus)
    ns = reduce(newSurplus)
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

#def need

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


# 414725 too high
# 141665 too low
def part1():
    """
    >>> part1()
    0
    """
    return example("input")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #print(example("example1"))