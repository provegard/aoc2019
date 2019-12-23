import intcode

class Computer:
    def __init__(self, program, address):
        self.program = program.copy()
        self.address = address
        self.state = None
        self.queue = [address]

    def joinNetwork(self, network):
        self.network = network

    def runOnce(self):
        inputs = self.queue
        if len(inputs) == 0:
            inputs = [-1]
        self.queue = []
        output = []
        self.state = intcode.run(self.program, inputs, output, self.state)
        self.network.send(output)

    def addToQueue(self, x, y):
        self.queue.append(x)
        self.queue.append(y)

class Network:
    def __init__(self, computers):
        self.computers = computers
        for c in computers:
            c.joinNetwork(self)

    def send(self, data):
        for i in range(0, len(data), 3):
            adr, x, y = data[i:i+3]
            print("sending %d/%d to %d" % (x, y, adr))
            comp = self.computers[adr]
            comp.addToQueue(x, y)
    
def part1():
    program = intcode.readProgram("input")
    computers = list(map(lambda a:Computer(program, a), range(0, 50)))
    network = Network(computers)

    while True:
        for c in computers:
            c.runOnce()


if __name__ == "__main__":
    part1() # 19530
