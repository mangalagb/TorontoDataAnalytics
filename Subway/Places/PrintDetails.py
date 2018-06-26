import json

with open('../Resources/subway_delays_map_data.txt', "r") as read_file:
        subway_file = json.load(read_file)
        for subway in subway_file:
            print(subway)

