
import math

def fuel(mass):
    return math.floor(mass / 3) - 2

def main():
    tot_fuel = 0
    with open("input") as f:
        for line in f.readlines():
            mass = int(line)
            f = fuel(mass)
            while f >= 0:
                tot_fuel += f
                f = fuel(f)

    print("total fuel = %d" % (tot_fuel,))

if __name__ == "__main__":
    main()