inputs = [int(line) for line in open("day1.txt")]

print(inputs)

total = 0
while (sum(inputs) > 0):
    outputs = [max(0, (x//3 - 2)) for x in inputs]

    print(outputs)

    print(sum(outputs))
    total += sum(outputs)
    inputs = outputs

print(total)
