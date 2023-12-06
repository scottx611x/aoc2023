import time
from functools import cached_property
from typing import List

start = time.time()

with open("input.txt") as f:
    data = f.readlines()

scratchers = []


class Scratcher:
    def __init__(self, card_number: int, my_numbers: List[int], winning_numbers: List[int]):
        self.card_number = card_number
        self.my_numbers = my_numbers
        self.winning_numbers = winning_numbers

    @cached_property
    def points(self) -> int:
        _points = 0
        for number in self.winning_numbers:
            if number in self.my_numbers:
                _points += 1
        return _points

    def __repr__(self):
        return f"<{self.__class__.__name__}: #: {self.card_number} points: {self.points}"


for line in data:
    card, data = line.split(":")
    card_number = int(card.split()[-1])
    numbers = data.split("|")
    winning_numbers = numbers[0].split()
    my_numbers = numbers[1].split()

    scratchers.append(Scratcher(card_number, my_numbers, winning_numbers))

for scratcher in scratchers:
    for i in range(scratcher.card_number + 1, scratcher.card_number + 1 + scratcher.points):
        scratchers.append(scratchers[i-1])

print(len(scratchers))
print('It took', time.time() - start, 'seconds.')