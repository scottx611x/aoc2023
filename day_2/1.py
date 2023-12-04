import re
import time

start = time.time()

valid_game_criteria = {
    "red": 12,
    "green": 13,
    "blue": 14
}

games_pattern = re.compile(r"Game\s(?P<game_id>\d+):\s(?P<game_data>.*)")
valid_game_ids = []


def is_valid_game(game) -> bool:
    for picks in game.split(","):
        n, color = picks.split()
        if int(n) > valid_game_criteria[color]:
            return False
    return True


with open("input.txt") as f:
    data = f.readlines()


for line in data:
    match = re.match(games_pattern, line)
    game_id = match.group("game_id")
    game_data = match.group("game_data")
    if all([is_valid_game(game) for game in game_data.split(";")]):
        valid_game_ids.append(int(game_id))


print(sum(valid_game_ids))
print('It took', time.time()-start, 'seconds.')