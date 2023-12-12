import re
import time

start = time.time()


with open("input.txt") as f:
    data = f.read() + "\n"


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class AlmanacMap:
    def __init__(self, name):
        self._match = re.search(fr"{name} map:\n((\d+\s)+)\n*", data).group(1).split()

    def __getitem__(self, key):
        key = int(key)

        for chunk in chunks(self._match, 3):
            destination_range_start, source_range_start, range_length = chunk
            sources = range(int(source_range_start), int(source_range_start) + int(range_length))
            destinations = range(int(destination_range_start), int(destination_range_start) + int(range_length))

            if key in sources:
                return destinations[sources.index(key)]

        return key


seeds = re.search("seeds:(.*)\n", data).group(1).split()
seed_to_soil_map = AlmanacMap("seed-to-soil")
soil_to_fertilizer_map = AlmanacMap("soil-to-fertilizer")
fertilizer_to_water_map = AlmanacMap("fertilizer-to-water")
water_to_light_map = AlmanacMap("water-to-light")
light_to_temperature_map = AlmanacMap("light-to-temperature")
temperature_to_humidity_map = AlmanacMap("temperature-to-humidity")
humidity_to_location_map = AlmanacMap("humidity-to-location")


lowest_location = None

for seed in seeds:
    location = humidity_to_location_map[
        temperature_to_humidity_map[
            light_to_temperature_map[
                water_to_light_map[
                    fertilizer_to_water_map[
                        soil_to_fertilizer_map[
                            seed_to_soil_map[seed]
                        ]
                    ]
                ]
            ]
        ]
    ]

    if lowest_location is None or int(location) < lowest_location:
        lowest_location = int(location)

print(lowest_location)
print('It took', time.time() - start, 'seconds.')