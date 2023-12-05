import re
import time

start = time.time()


class SchematicMatch:
    def __init__(self, line_number: int, match: re.Match):
        self.match = match
        self.line_number = line_number
        _start_pos, _end_pos = self.match.span()
        self.start_pos = _start_pos
        self.end_pos = _end_pos - 1  # this just made it easier for me to reason about while debugging some edge-cases

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.match.group()} line: {self.line_number}, start: {self.start_pos}, end: {self.end_pos}>"


class Symbol(SchematicMatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.part_numbers = []
        self._is_gear = False

    def has_adjacent_part_number(self, part: "PartNumber") -> bool:
        match_bounds = list(range(self.start_pos - 1, self.end_pos + 2))
        _has_adjacent_part = any(x in list(range(part.start_pos, part.end_pos + 1)) for x in match_bounds)
        return _has_adjacent_part

    def is_gear(self, index: int, schematic_lines) -> bool:
        if self._is_gear:
            return True

        if not self.match.group() == "*":
            return False

        part_numbers_to_check = schematic_lines[index]["numbers"] + schematic_lines[index + 1]["numbers"] + schematic_lines[index - 1]["numbers"]

        for part_number in part_numbers_to_check:
            if self.has_adjacent_part_number(part_number):
                self.part_numbers.append(part_number)

        self._is_gear = len(self.part_numbers) == 2
        return self._is_gear

    @property
    def gear_ratio(self):
        if not self._is_gear:
            raise RuntimeError("Can't compute gear ratio for non-gear")
        return self.part_numbers[0].part_number * self.part_numbers[1].part_number


class PartNumber(SchematicMatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.part_number = int(self.match.group())


schematic_lines = {}
valid_gears = set()

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

    for symbol_match in schematic_lines[index]["symbols"]:
        if symbol_match.is_gear(index, schematic_lines):
            valid_gears.add(symbol_match)


print(sum([g.gear_ratio for g in valid_gears]))
print('It took', time.time() - start, 'seconds.')