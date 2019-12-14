import sys

inputs = next(open("day5.txt"))

original_program = list(map(int, inputs.strip().split(","))) + ([0] * 100)


for noun in range(100):
    for verb in range(100):
        program = original_program[:]

        program[1] = noun
        program[2] = verb

        pc = 0

        while program[pc] != 99:
            print(program[pc:pc+4])
            x = program[pc+1]
            y = program[pc+2]
            z = program[pc+3]
            if program[pc] == 1:
                program[z] = program[x] + program[y]
            if program[pc] == 2:
                program[z] = program[x] * program[y]
            pc += 4

        if (program[0] == 19690720):
            print(100*noun + verb)
            sys.exit()

