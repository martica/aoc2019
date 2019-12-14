count = 0
for i in range(264360, 746325):
    numbers = [int(d) for d in str(i)]
    adjancent = ( 
                                         numbers[0] == numbers[1] and numbers[1] != numbers[2] or 
            numbers[0] != numbers[1] and numbers[1] == numbers[2] and numbers[2] != numbers[3] or 
            numbers[1] != numbers[2] and numbers[2] == numbers[3] and numbers[3] != numbers[4] or 
            numbers[2] != numbers[3] and numbers[3] == numbers[4] and numbers[4] != numbers[5] or 
            numbers[3] != numbers[4] and numbers[4] == numbers[5])
    in_order = sorted(numbers) == numbers

    if adjancent and in_order:
        print(i)
        count = count + 1

print(count)

