import re
import time
from typing import List

start = time.time()


class SchematicMatch:
    def __init__(self, line_number: int, match: re.Match):
        self.match = match
        self.line_number = line_number
        self.start_pos, self.end_pos = self.match.span()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.match.group()} line: {self.line_number}, start: {self.start_pos}, end: {self.end_pos}>"


class Symbol(SchematicMatch):
    pass


class PartNumber(SchematicMatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.part_number = int(self.match.group())

    def is_adjacent_to_symbol(self, symbols: List[Symbol]) -> bool:
        for symbol in symbols:
            match_bounds = list(range(self.start_pos, self.end_pos + 1))
            if any([symbol.start_pos in match_bounds, symbol.end_pos in match_bounds]):
                return True

        return False


schematic_lines = {}
valid_part_numbers = set()

with open("input.txt") as f:
    data = f.readlines()

for index, schematic_line in enumerate(data):
    schematic_lines[index] = {
        "numbers": [PartNumber(index, part_number) for part_number in list(re.finditer(r"\d+", schematic_line))],
        "symbols": [Symbol(index, symbol) for symbol in list(re.finditer(r"[^0-9.\n]+", schematic_line))]
    }

    # Just populate the 0th schematic_lines record so that I can do this in one pass
    if index == 0:
        data += [""]
        continue

    index = index - 1

    for number_match in schematic_lines[index]["numbers"]:
        if number_match.is_adjacent_to_symbol(schematic_lines[index]["symbols"]):
            valid_part_numbers.add(number_match)

        line_before = index - 1
        line_after = index + 1

        for line_num in [line_before, line_after]:
            if line_num > len(data) or line_num < 0:
                continue

            if number_match.is_adjacent_to_symbol(schematic_lines[line_num]["symbols"]):
                valid_part_numbers.add(number_match)

print(sum([i.part_number for i in valid_part_numbers]))
print('It took', time.time() - start, 'seconds.')