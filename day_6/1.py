import math
import re
import time

start = time.time()

with open("input.txt") as f:
    data = f.read() + "\n"

times = re.findall("Time:(.*)\n", data)[0].split()
distances = re.findall("Distance:(.*)\n", data)[0].split()

races = {i: {"time": t, "distance": distances[i]} for i, t in enumerate(times)}


def get_race_win_options(race_duration: int, winning_distance: int) -> int:
    race_wins = 0

    for milliseconds_held in range(0, race_duration):
        distance_traveled = (race_duration - milliseconds_held) * milliseconds_held
        if distance_traveled > winning_distance:
            race_wins += 1

    return race_wins


for race in races.values():
    race["win_options"] = get_race_win_options(int(race["time"]), int(race["distance"]))


print(math.prod(r["win_options"] for r in races.values()))
print('It took', time.time() - start, 'seconds.')