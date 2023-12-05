import time

start = time.time()

with open("input.txt") as f:
    data = f.readlines()

total = 0

for line in data:
    card, data = line.split(":")
    numbers = data.split("|")
    winning_numbers = numbers[0].split()
    my_numbers = numbers[1].split()

    points = 0
    for number in winning_numbers:
        if number in my_numbers:
            points = points + 1 if not points else points * 2

    total += points

print(total)
print('It took', time.time() - start, 'seconds.')