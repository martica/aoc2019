import collections
import enum


class IndexingMode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Instruction:
    def __init__(self, indexing_modes, parameters, computer):
        self.indexing_modes = indexing_modes
        self.parameters = parameters
        self.computer = computer

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.parameters, self.indexing_modes)

    def read(self, parameter_number):
        return self.computer.read(self.parameters[parameter_number], self.indexing_modes[parameter_number])

    def write(self, parameter_number, value):
        return self.computer.write(self.parameters[parameter_number], self.indexing_modes[parameter_number], value)


class Add(Instruction):
    size = 4

    def execute(self, computer):
        self.write(2, self.read(0) + self.read(1))
        return computer.pc + self.size


class Multiply(Instruction):
    size = 4

    def execute(self, computer):
        self.write(2, self.read(0) * self.read(1))
        return computer.pc + self.size


class Input(Instruction):
    size = 2

    def execute(self, computer):
        value = computer.inputs.pop(0)  # int(input())
        assert value is not None, "Not enough inputs"
        self.write(0, value)
        return computer.pc + self.size


class Output(Instruction):
    size = 2

    def execute(self, computer):
        value = self.read(0)
        computer.output.append(value)
        return computer.pc + self.size


class JumpIfTrue(Instruction):
    size = 3

    def execute(self, computer):
        if self.read(0):
            return self.read(1)
        return computer.pc + self.size


class JumpIfFalse(Instruction):
    size = 3

    def execute(self, computer):
        if not self.read(0):
            return self.read(1)
        return computer.pc + self.size


class LessThan(Instruction):
    size = 4

    def execute(self, computer):
        left_hand = self.read(0)
        right_hand = self.read(1)
        output = 0
        if left_hand < right_hand:
            output = 1
        self.write(2, output)
        return computer.pc + self.size


class Equals(Instruction):
    size = 4

    def execute(self, computer):
        left_hand = self.read(0)
        right_hand = self.read(1)
        output = 0
        if left_hand == right_hand:
            output = 1
        self.write(2, output)
        return computer.pc + self.size


class AdjustRelativeBase(Instruction):
    size = 2

    def execute(self, computer):
        offset = self.read(0)
        computer.rb += offset
        return computer.pc + self.size


class Memory:
    def __init__(self):
        self.memory = collections.defaultdict(int)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self.memory[offset] for offset in range(*key.indices(key.stop))]
        return self.memory[key]

    def __setitem__(self, key, value):
        self.memory[key] = value


OPCODES = [None, Add, Multiply, Input, Output, JumpIfTrue, JumpIfFalse, LessThan, Equals, AdjustRelativeBase]


class Computer:
    def __init__(self, program, inputs, debug=False):
        self.memory = Memory()
        self.pc = 0
        self.rb = 0
        self.output = []
        self.inputs = inputs
        self.debug = debug

        for offset, value in enumerate(map(int, program.strip().split(","))):
            self.memory[offset] = value

    def run(self, inputs):
        self.inputs.extend(inputs)
        while self.memory[self.pc] % 100 != 99 and not self.output:
            instruction = self.decode()
            if self.debug:
                print(instruction)
            self.pc = instruction.execute(self)

        if self.output:
            return self.output.pop()

        return None

    def decode(self):
        opcode = self.memory[self.pc] % 100
        instruction = OPCODES[opcode]

        indexing_modes = list(reversed([IndexingMode(int(x)) for x in "%03d" % (self.memory[self.pc] // 100)]))[
                         :instruction.size]
        parameters = self.memory[self.pc + 1: self.pc + instruction.size + 1]

        assert opcode < len(OPCODES), "Unknown instruction: %s" % self.memory[self.pc]
        return instruction(indexing_modes, parameters, self)

    def read(self, index, indexing_mode):
        value = None
        if indexing_mode == IndexingMode.IMMEDIATE:
            value = index
        if indexing_mode == IndexingMode.POSITION:
            value = self.memory[index]
        if indexing_mode == IndexingMode.RELATIVE:
            value = self.memory[self.rb + index]
        if self.debug:
            print("read(%s %s) == %s" % (index, indexing_mode, value))
        return value

    def write(self, index, indexing_mode, value):
        assert indexing_mode != IndexingMode.IMMEDIATE, "Cannot write with indexing mode IMMEDIATE"
        if indexing_mode == IndexingMode.POSITION:
            self.memory[index] = value
        if indexing_mode == IndexingMode.RELATIVE:
            self.memory[self.rb + index] = value
