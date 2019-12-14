inputs = [line.strip().split(")") for line in open("day6.txt")]
#inputs = [line.strip().split(")") for line in open("day6example.txt")]


class Orbit:
    def __init__(self, center):
        self.center = center
        if self.center == 'COM':
            self.orbit_count = 1
        else:
            self.orbit_count = None

    def __repr__(self):
        return "Orbit(%s) == %s" % (self.center, self.orbit_count)


def calculate_orbit_count(orbit, orbits):
    if orbit.orbit_count is None:
        orbit.orbit_count = 1 + calculate_orbit_count(orbits[orbit.center], orbits)

    return orbit.orbit_count


def main():
    orbits = dict()

    for input in inputs:
        orbits[input[1]] = Orbit(input[0])

    total_orbits = 0
    for orbit in orbits.values():
        total_orbits += calculate_orbit_count(orbit, orbits)


    print(total_orbits)

if __name__ == '__main__':
    main()
