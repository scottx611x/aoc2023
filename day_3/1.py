import re
import time
from typing import List

start = time.time()

with open("input.txt") as f:
    data = f.readlines()


class Matched:
    def __init__(self, line_number: int, match: re.Match):
        self.match = match
        self.line_number = line_number
        self.start_pos, self.end_pos = self.match.span()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.match.group()} line: {self.line_number}, start: {self.start_pos}, end: {self.end_pos}"


class Symbol(Matched):
    pass


class PartNumber(Matched):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.part_number = int(self.match.group())

    def is_adjacent_to_symbol(self, symbols: List[Symbol]) -> bool:
        for symbol in symbols:
            if self.line_number == symbol.line_number:
                if self.start_pos == symbol.end_pos or symbol.start_pos == self.end_pos:
                    return True

            else:
                match_bounds = list(range(self.start_pos, self.end_pos+1))
                if any([symbol.start_pos in match_bounds, symbol.end_pos in match_bounds]):
                    return True

        return False


schematic_lines = {}
valid_part_numbers = set()

for i, line in enumerate(data):
    number_matches = [PartNumber(i, j) for j in list(re.finditer(r"\d+", line))]
    symbol_matches = [Symbol(i, j) for j in list(re.finditer(r"[^0-9.\n]+", line))]

    schematic_lines[i] = {
        "number_matches": number_matches,
        "symbol_matches": symbol_matches
    }

for i in schematic_lines.keys():
    for number_match in schematic_lines[i]["number_matches"]:
        if number_match.is_adjacent_to_symbol(schematic_lines[i]["symbol_matches"]):
            valid_part_numbers.add(number_match)

        try:
            if number_match.is_adjacent_to_symbol(schematic_lines[i - 1]["symbol_matches"]):
                valid_part_numbers.add(number_match)
        except KeyError:
            pass

        try:
            if number_match.is_adjacent_to_symbol(schematic_lines[i + 1]["symbol_matches"]):
                valid_part_numbers.add(number_match)
        except KeyError:
            pass


print(sum([i.part_number for i in valid_part_numbers]))
print('It took', time.time() - start, 'seconds.')