import intcode

def draw(output):
    def toStr(x):
        if x > 127:
            return str(x)
        return chr(x)

    chars = list(map(toStr, output))
    print("".join(chars))

def splitStr(word): return [char for char in word]
def toAscii(inp):
    return list(map(ord, splitStr(inp)))
if __name__ == "__main__":
    program = intcode.readProgram("input")
    output = []

    # springdroid jumps 4 tiles (lands 4 tiles from the current one),
    # i.e. can jump over a hole 3 tiles wide
    code1 = [
        "NOT C J",
        "AND D J",
        "NOT A T",
        "OR T J",
        "WALK"
    ] # --> 19354818
    code2 = [
        "NOT A J",
        "AND D J",
        "NOT B T",
        "AND D T",
        "OR T J",
        "NOT C T",
        "AND D T",
        "AND H T",
        "OR T J",
        "RUN"
    ] # --> 1143787220

    inputs = toAscii("\n".join(code2) + "\n")

    state = intcode.run(program, inputs, output)
    draw(output)