import re
import time

start = time.time()


with open("input.txt") as f:
    data = f.read() + "\n"


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class ReverseAlmanacMap:
    def __repr__(self):
        return "-".join(reversed(self.name.split("-")))

    def __init__(self, name):
        self.name = name
        self._match = re.search(fr"{name} map:\n((\d+\s)+)\n*", data).group(1).split()
        self._ranges = {}

        for _chunk in chunks(self._match, 3):
            destination_range_start, source_range_start, range_length = _chunk
            sources = range(int(source_range_start), int(source_range_start) + int(range_length))
            destinations = range(int(destination_range_start), int(destination_range_start) + int(range_length))
            self._ranges[destinations] = sources

    def __getitem__(self, key: int):
        for destinations in self._ranges:
            if key in destinations:
                return self._ranges[destinations][destinations.index(key)]
        return key


soil_to_seed_map = ReverseAlmanacMap("seed-to-soil")
fertilizer_to_soil_map = ReverseAlmanacMap("soil-to-fertilizer")
water_to_fertilizer_map = ReverseAlmanacMap("fertilizer-to-water")
light_to_water_map = ReverseAlmanacMap("water-to-light")
temperature_to_light_map = ReverseAlmanacMap("light-to-temperature")
humidity_to_temperature_map = ReverseAlmanacMap("temperature-to-humidity")
location_to_humidity_map = ReverseAlmanacMap("humidity-to-location")


lowest_location = None


def has_valid_seed(location, seeds) -> bool:
    seed = soil_to_seed_map[
        fertilizer_to_soil_map[
            water_to_fertilizer_map[
                light_to_water_map[
                    temperature_to_light_map[
                        humidity_to_temperature_map[
                            location_to_humidity_map[location]
                        ]
                    ]
                ]
            ]
        ]
    ]
    return any(seed in r for r in seeds)


seeds = []

for chunk in list(chunks(re.search("seeds:(.*)\n", data).group(1).split(), 2)):
    seed_start, seed_range = chunk
    seeds.append(range(int(seed_start), int(seed_start) + int(seed_range)))

# It's slow, but I couldn't figure out a quicker way. I'm just performing
# reverse lookups on the nested dict/Sankey diagram-like data
for location in range(0, sorted(seeds, key=lambda s: s.start)[-1].stop):
    if has_valid_seed(location, seeds):
        print(f"Lowest location is: {location}")
        break

print('It took', time.time() - start, 'seconds.')