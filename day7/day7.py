import collections
import itertools
import sys


class Computer:
    def __init__(self, program, inputs):
        self.memory = collections.defaultdict(int)
        self.pc = 0
        self.output = []
        self.inputs = inputs

        for offset, value in enumerate(map(int, program.strip().split(","))):
            self.memory[offset] = value

    def run(self, inputs):
        self.inputs.extend(inputs)
        while self.memory[self.pc] % 100 != 99 and not self.output:
            instruction = decode(self.memory, self.pc)
            self.pc = instruction.execute(self)

        if self.output:
            return self.output.pop()

        return None

    def read(self, index, indexing_mode):
        if indexing_mode == 0:
            return self.memory[index]
        return index

    def write(self, index, value):
        self.memory[index] = value


class Instruction:
    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.parameters, self.indexing_modes)


class Add(Instruction):
    def __init__(self, indexing_modes, parameters):
        self.size = 4
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, computer):
        addends = [
            computer.read(self.parameters[0], self.indexing_modes[0]),
            computer.read(self.parameters[1], self.indexing_modes[1])
        ]
        computer.write(self.parameters[2], sum(addends))
        return computer.pc + self.size


class Multiply(Instruction):
    def __init__(self, indexing_modes, parameters):
        self.size = 4
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, computer):
        multiplicands = [
            computer.read(self.parameters[0], self.indexing_modes[0]),
            computer.read(self.parameters[1], self.indexing_modes[1])
        ]
        computer.write(self.parameters[2], multiplicands[0] * multiplicands[1])
        return computer.pc + self.size


class Input(Instruction):
    def __init__(self, indexing_modes, parameters):
        self.size = 2
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, computer):
        value = computer.inputs.pop(0)  # int(input())
        assert value is not None, "Not enough inputs"
        computer.write(self.parameters[0], value)
        return computer.pc + self.size


class Output(Instruction):
    def __init__(self, indexing_modes, parameters):
        self.size = 2
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, computer):
        value = computer.read(self.parameters[0], self.indexing_modes[0])
        #print(value)
        computer.output.append(value)
        return computer.pc + self.size


class JumpIfTrue(Instruction):
    def __init__(self, indexing_modes, parameters):
        self.size = 3
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, computer):
        if computer.read(self.parameters[0], self.indexing_modes[0]):
            return computer.read(self.parameters[1], self.indexing_modes[1])
        return computer.pc + self.size


class JumpIfFalse(Instruction):
    def __init__(self, indexing_modes, parameters):
        self.size = 3
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, computer):
        if not computer.read(self.parameters[0], self.indexing_modes[0]):
            return computer.read(self.parameters[1], self.indexing_modes[1])
        return computer.pc + self.size


class LessThan(Instruction):
    def __init__(self, indexing_modes, parameters):
        self.size = 4
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, computer):
        left_hand = computer.read(self.parameters[0], self.indexing_modes[0])
        right_hand = computer.read(self.parameters[1], self.indexing_modes[1])
        output = 0
        if left_hand < right_hand:
            output = 1
        computer.write(self.parameters[2], output)
        return computer.pc + self.size


class Equals(Instruction):
    def __init__(self, indexing_modes, parameters):
        self.size = 4
        self.indexing_modes = indexing_modes
        self.parameters = parameters

    def execute(self, computer):
        left_hand = computer.read(self.parameters[0], self.indexing_modes[0])
        right_hand = computer.read(self.parameters[1], self.indexing_modes[1])
        output = 0
        if left_hand == right_hand:
            output = 1
        computer.write(self.parameters[2], output)
        return computer.pc + self.size


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
    program_text = next(open("day7.txt"))

    largest_output = 0
    best_combination = None
    for a, b, c, d, e in itertools.permutations(range(5, 10)):
        print(a, b, c, d, e, end=' ')
        amp1 = Computer(program_text, [a])
        amp2 = Computer(program_text, [b])
        amp3 = Computer(program_text, [c])
        amp4 = Computer(program_text, [d])
        amp5 = Computer(program_text, [e])

        output5 = 0
        new_output5 = "something"
        while new_output5 is not None:
            output1 = amp1.run([output5])
            print(repr(output1), end=' ')
            output2 = amp2.run([output1])
            print(repr(output2), end=' ')
            output3 = amp3.run([output2])
            print(repr(output3), end=' ')
            output4 = amp4.run([output3])
            print(repr(output4), end=' ')
            new_output5 = amp5.run([output4])
            if new_output5 is not None:
                output5 = new_output5
            print(repr(output5))

        if output5 > largest_output:
            largest_output = output5
            best_combination = (a, b, c, d, e)

    print(largest_output)
    print(best_combination)


if __name__ == "__main__":
    main()
