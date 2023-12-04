import re
import time
from functools import reduce

start = time.time()

games_pattern = re.compile(r"Game\s(?P<game_id>\d+):\s(?P<game_data>.*)")
cube_powers = []


with open("input.txt") as f:
    data = f.readlines()


for line in data:
    match = re.match(games_pattern, line)
    game_id = match.group("game_id")
    game_data = match.group("game_data")
    power_picks = {}
    for game in game_data.split(";"):
        for picks in game.split(","):
            n, color = picks.split()
            if power_picks.get(color, 0) < int(n):
                power_picks[color] = int(n)

    cube_powers.append(
        reduce((lambda x, y: x * y), power_picks.values())
    )


print(sum(cube_powers))
print('It took', time.time()-start, 'seconds.')