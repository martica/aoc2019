import itertools
from intcode.computer import Computer

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
