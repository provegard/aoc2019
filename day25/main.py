import intcode
import itertools

def rendered(output):
    def toStr(x):
        if x > 127 or x < 0:
            return str(x)
        return chr(x)

    chars = list(map(toStr, output))
    return "".join(chars)

def splitStr(word): return [char for char in word]
def toAscii(inp):
    return list(map(ord, splitStr(inp)))

def runWithCommands(program, state, commands):
    inp = []
    while True:
        output = []
        state = intcode.run(program, inp, output, state)
        r = rendered(output)
        print(r)

        if r.find("Pressure-Sensitive Floor") >= 0 and r.find("Alert") < 0:
            raise Exception("Done")

        if len(commands) == 0:
            # nothing more to do
            break

        line = commands.pop(0)
        print("using input: %s" % (line,))
        inp = toAscii(line + "\n")
    return state


def part1():
    program = intcode.readProgram("input")

    moveCommands = [
        "west",
        "take pointer",
        "east",
        "south",
        "take whirled peas",
        "south",
        "south",
        "south",
        "take festive hat",
        "north",
        "north",
        "north",
        "north",
        "north",
        "take coin",
        "north",
        "take astronaut ice cream",
        "north",
        "west",
        "take dark matter",
        "south",
        "take klein bottle",
        "west",
        "take mutex",
        "west",
        "south",
        "inv"
    ]

    inv = [
        "mutex",
        "dark matter",
        "astronaut ice cream",
        "festive hat",
        "whirled peas",
        "coin",
        "klein bottle",
        "pointer"
    ]
    dropCommands = list(map(lambda x:"drop %s" % (x,), inv))

    invCombos = []
    for L in range(0, len(inv)+1):
        for subset in itertools.combinations(inv, L):
            invCombos.append(subset)

    state = None
    state = runWithCommands(program, state, moveCommands)
    state = runWithCommands(program, state, dropCommands)
    while len(invCombos) > 0:
        tryState = intcode.cloneState(state)

        tryCommands = []
        combo = invCombos.pop(0)
        print("combo: %s" % (combo,))
        # Take the items
        for c in combo:
            tryCommands.append("take %s" % (c,))
        # Move east
        tryCommands.append("east")

        runWithCommands(program, tryState, tryCommands)


if __name__ == "__main__":
    part1()