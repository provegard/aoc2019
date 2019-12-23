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

    def isIdle(self):
        return len(self.queue) == 0

class NAT:
    def __init__(self, computers):
        self.computers = computers
        self.x = None
        self.y = None
        self.lastYTo0 = None

    def send(self, x, y):
        self.x = x
        self.y = y

    def process(self):
        idleStates = list(map(lambda c:c.isIdle(), self.computers))
        allIdle = all(idleStates)
        if allIdle and not (self.x is None):
            if self.lastYTo0 == self.y:
                raise Exception("sending %d to address 0 twice in a row" % (self.y,))
            self.computers[0].addToQueue(self.x, self.y)
            self.lastYTo0 = self.y

class Network:
    def __init__(self, computers, nat):
        self.computers = computers
        for c in computers:
            c.joinNetwork(self)
        self.nat = nat

    def send(self, data):
        for i in range(0, len(data), 3):
            adr, x, y = data[i:i+3]
            if adr == 255:
                print("sending %d/%d to NAT" % (x, y))
                self.nat.send(x, y)
            else:
                print("sending %d/%d to %d" % (x, y, adr))
                comp = self.computers[adr]
                comp.addToQueue(x, y)
    
def run():
    program = intcode.readProgram("input")
    computers = list(map(lambda a:Computer(program, a), range(0, 50)))
    nat = NAT(computers)
    network = Network(computers, nat)

    while True:
        for c in computers:
            c.runOnce()
        nat.process()


if __name__ == "__main__":
    #run() # 19530
    run() # 12725