import collections
import sys


def read(memory, index, indexing_mode):
    if indexing_mode == 0:
        return memory[index]
    return index


def write(memory, index, value):
    memory[index] = value


class Add:
    def __init__(self, indexing_modes, parameters):
        self.size = 4
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, pc, memory):
        addends = [
            read(memory, self.parameters[0], self.indexing_modes[0]),
            read(memory, self.parameters[1], self.indexing_modes[1])
        ]
        write(memory, self.parameters[2], sum(addends))
        return pc + self.size


class Multiply:
    def __init__(self, indexing_modes, parameters):
        self.size = 4
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, pc, memory):
        multiplicands = [
            read(memory, self.parameters[0], self.indexing_modes[0]),
            read(memory, self.parameters[1], self.indexing_modes[1])
        ]
        write(memory, self.parameters[2], multiplicands[0] * multiplicands[1])
        return pc + self.size


class Input:
    def __init__(self, indexing_modes, parameters):
        self.size = 2
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, pc, memory):
        write(memory, self.parameters[0], int(input()))
        return pc + self.size


class Output:
    def __init__(self, indexing_modes, parameters):
        self.size = 2
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, pc, memory):
        print(read(memory, self.parameters[0], self.indexing_modes[0]))
        return pc + self.size


class JumpIfTrue:
    def __init__(self, indexing_modes, parameters):
        self.size = 3
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, pc, memory):
        if read(memory, self.parameters[0], self.indexing_modes[0]):
            return read(memory, self.parameters[1], self.indexing_modes[1])
        return pc + self.size


class JumpIfFalse:
    def __init__(self, indexing_modes, parameters):
        self.size = 3
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, pc, memory):
        if not read(memory, self.parameters[0], self.indexing_modes[0]):
            return read(memory, self.parameters[1], self.indexing_modes[1])
        return pc + self.size


class LessThan:
    def __init__(self, indexing_modes, parameters):
        self.size = 4
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, pc, memory):
        left_hand = read(memory, self.parameters[0], self.indexing_modes[0])
        right_hand = read(memory, self.parameters[1], self.indexing_modes[1])
        output = 0
        if left_hand < right_hand:
            output = 1
        write(memory, self.parameters[2], output)
        return pc + self.size


class Equals:
    def __init__(self, indexing_modes, parameters):
        self.size = 4
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, pc, memory):
        left_hand = read(memory, self.parameters[0], self.indexing_modes[0])
        right_hand = read(memory, self.parameters[1], self.indexing_modes[1])
        output = 0
        if left_hand == right_hand:
            output = 1
        write(memory, self.parameters[2], output)
        return pc + self.size


def decode(memory, pc):
    opcode = memory[pc] % 100
    indexing_modes = list(reversed([int(x) for x in "%03d" % (memory[pc] // 100)]))
    if opcode == 1:
        return Add(indexing_modes, [memory[pc + 1], memory[pc + 2], memory[pc + 3]])
    if opcode == 2:
        return Multiply(indexing_modes, [memory[pc + 1], memory[pc + 2], memory[pc + 3]])
    if opcode == 3:
        return Input(indexing_modes, [memory[pc + 1]])
    if opcode == 4:
        return Output(indexing_modes, [memory[pc + 1]])
    if opcode == 5:
        return JumpIfTrue(indexing_modes, [memory[pc + 1], memory[pc + 2]])
    if opcode == 6:
        return JumpIfFalse(indexing_modes, [memory[pc + 1], memory[pc + 2]])
    if opcode == 7:
        return LessThan(indexing_modes, [memory[pc + 1], memory[pc + 2], memory[pc + 3]])
    if opcode == 8:
        return Equals(indexing_modes, [memory[pc + 1], memory[pc + 2], memory[pc + 3]])
    assert False, "Unknown instruction: %s" % memory[pc]


def main():
    inputs = next(open("day5.txt"))

    memory = collections.defaultdict(int)

    for offset, value in enumerate(map(int, inputs.strip().split(","))):
        memory[offset] = value

    print(memory)

    pc = 0

    while memory[pc] % 100 != 99:
        instruction = decode(memory, pc)
        pc = instruction.execute(pc, memory)


if __name__ == "__main__":
    main()
