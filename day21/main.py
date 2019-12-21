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

    code = [
        "NOT C J",
        "AND D J",
        "NOT A T",
        "OR T J",
        "WALK"
    ]

    inputs = toAscii("\n".join(code) + "\n")

    state = intcode.run(program, inputs, output)
    draw(output) # 19354818