import collections
import itertools
import enum


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT


class Color(enum.IntEnum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2


class Layer:
    def __init__(self, pixels):
        self.pixels = [Color(int(pixel)) for pixel in pixels]

    def count(self, value):
        return sum(1 for pixel in self.pixels if pixel == value)

    def pixel(self, x, y):
        return self.pixels[y*WIDTH + x]

    def __repr__(self):
        return repr(collections.Counter(self.pixels))


class LayerStack:
    def __init__(self, layers):
        self.layers = layers

    def color(self, x, y):
        """ Find the value of the pixel at a x, y
        :param x: the horizontal position
        :param y: the vertical position
        :return: Color
        """
        color = Color.TRANSPARENT

        for layer in self.layers:
            color = layer.pixel(x, y)
            if color != Color.TRANSPARENT:
                return color

        return color


def main():
    input_data = next(open("input.txt", "r")).strip()

    layers = [Layer(layer_data) for layer_data in grouper(input_data, LAYER_SIZE)]
    image = LayerStack(layers)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel = image.color(x, y)
            if pixel == Color.BLACK:
                output = " "
            else:
                output = "X"
            print(output, end="")
        print("")


if __name__ == '__main__':
    main()
