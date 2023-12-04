SUM = 0

with open("input_day_1.txt") as f:
    data = f.readlines()

for line in data:
    numbers = list(filter(str.isdigit, line))
    SUM += int(f"{numbers[0]}{numbers[-1]}")

print(SUM)