import googlemaps
import json

API_KEY = ""


def get_subway_coordinates():
    subway_delays = read_subway_station_delays()
    get_subway_station_names(subway_delays)


def read_subway_station_delays():
    with open("../Resources/subway_delays.txt", "r") as read_file:
        return json.load(read_file)


def get_subway_station_names(subway_delays):
    print("Getting names of all subway stations...")
    subway_names = []
    for subway_name in subway_delays:
        if subway_name[1] is not 0:
            name = subway_name[0].split("(", 1)[0]
            subway_names.append([name, subway_name[1]])
    get_coordinates(subway_names)


def get_coordinates(subway_names):
    print("Getting latitude and longitude coordinates for the subway stations...")
    read_key()
    subway_with_coordinates = []
    try:
        for subway in subway_names:
            name = subway[0]
            coordinates = send_request(name)
            subway_with_coordinates.append([name, subway[1], list(coordinates.items())])
    except:
        print("error")
    write_to_file(subway_with_coordinates)


def send_request(name):
    gmaps = googlemaps.Client(key=API_KEY)

    # Geocoding an address
    geocode_result = gmaps.geocode(name)
    coordinates = geocode_result[0]["geometry"]["location"]
    return coordinates


def read_key():
    with open('../Resources/API_Key', 'r') as my_file:
        global API_KEY
        API_KEY = my_file.read().replace('\n', '')


def write_to_file(subway_data):
    print("Writing info to file...")
    with open('../Resources/subway_delays_map_data.txt', 'w') as file:
        file.write(json.dumps(subway_data))
    print("All done!")

get_subway_coordinates()
