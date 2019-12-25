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

def part1():
    program = intcode.readProgram("input")

    commands = [
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
    tryCommands = []

    state = None
    inp = []
    while True:
        output = []
        state = intcode.run(program, inp, output, state)
        r = rendered(output)
        print(r)

        if r.find("Pressure-Sensitive Floor") >= 0 and r.find("Alert") < 0:
            print("DONE?")
            break

        if len(commands) > 0:
            # Collect stuff and go to Security Checkpoint
            line = commands.pop(0)
        elif len(dropCommands) > 0:
            # Drop everything
            line = dropCommands.pop(0)
        elif len(tryCommands) > 0:
            line = tryCommands.pop(0)
        elif len(invCombos) > 0:
            combo = invCombos.pop(0)
            # Take the items
            for c in combo:
                tryCommands.append("take %s" % (c,))
            # Move east
            tryCommands.append("east")
            # Drop the items
            for c in combo:
                tryCommands.append("drop %s" % (c,))
            
            # execute the first one
            line = tryCommands.pop(0)
        else:
            line = input("enter> ")

        print("using input: %s" % (line,))
        inp = toAscii(line + "\n")


if __name__ == "__main__":
    part1()