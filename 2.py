import re

SUM = 0

number_map = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

pattern = re.compile(r"(?=(" + "|".join(number_map.keys()) + "|[0-9]))")

with open("input_day_1.txt") as f:
    data = f.readlines()

for line in data:
    matches = list(re.finditer(pattern, line))

    first = matches[0].group(1)
    last = matches[-1].group(1)
    SUM += int(f"{number_map.get(first,first)}{number_map.get(last,last)}")

print(SUM)