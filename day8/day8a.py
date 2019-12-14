import collections
import itertools


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT


class Layer:
    def __init__(self, pixels):
        print(len(pixels))
        self.pixels = [int(pixel) for pixel in pixels]

    def count(self, value):
        return sum(1 for pixel in self.pixels if pixel == value)

    def __repr__(self):
        return repr(collections.Counter(self.pixels))


def main():
    input_data = next(open("input.txt", "r")).strip()

    layers = [Layer(layer_data) for layer_data in grouper(input_data, LAYER_SIZE)]

    sorted_layers = sorted(layers, key=lambda layer: layer.count(0))

    print(sorted_layers)
    print(sorted_layers[0].count(1) * sorted_layers[0].count(2))


if __name__ == '__main__':
    main()
