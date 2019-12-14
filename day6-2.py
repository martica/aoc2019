inputs = [line.strip().split(")") for line in open("day6.txt")]


class Orbit:
    def __init__(self, center):
        self.center = center
        if self.center == 'COM':
            self.orbit_count = 1
        else:
            self.orbit_count = None

    def __repr__(self):
        return "Orbit(%s) == %s" % (self.center, self.orbit_count)




def main():
    orbits = dict()

    for input in inputs:
        orbits[input[1]] = Orbit(input[0])

    our_chain = []
    santa_chain = []

    location = 'YOU'
    while location != 'COM':
        location = orbits[location].center
        our_chain.append(location)

    location = 'SAN'
    while location != 'COM':
        location = orbits[location].center
        santa_chain.append(location)

    print(our_chain)
    print(santa_chain)

    index = -1
    while our_chain[index] == santa_chain[index]:
        index -= 1

    print(our_chain[index:-1])
    print(santa_chain[index:-1])

    print(len(our_chain) + len(santa_chain) + index * 2 + 2)

if __name__ == '__main__':
    main()
