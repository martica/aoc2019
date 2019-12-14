import itertools
from intcode.computer import Computer

def main():
    program_text = next(open("input.txt"))

    computer = Computer(program_text, [1], debug=True)

    output = computer.run([])
    print(output)
    while output is not None:
        output = computer.run([])
        print(output)

if __name__ == "__main__":
    main()
