import re
import time

start = time.time()

with open("input.txt") as f:
    data = f.read() + "\n"

race_duration = int(re.findall("Time:(.*)\n", data)[0].replace(" ", ""))
winning_distance = int(re.findall("Distance:(.*)\n", data)[0].replace(" ", ""))


def get_first_race_win(_range: range, duration: int = race_duration, distance: int = winning_distance) -> int:
    for milliseconds_held in _range:
        distance_traveled = (duration - milliseconds_held) * milliseconds_held
        if distance_traveled > distance:
            return milliseconds_held


begin = get_first_race_win(range(0, race_duration))
end = get_first_race_win(range(race_duration, 0, -1))


print(len(range(begin, end + 1)))
print('It took', time.time() - start, 'seconds.')