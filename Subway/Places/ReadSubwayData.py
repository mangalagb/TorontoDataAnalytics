import pandas as pd
import operator
import json

# # may 2017 to april 2018
subway_delays = {}

files = ['may2017.xlsx', 'june2017.xlsx', 'july2017.xlsx', 'aug2017.xlsx',
         'sep2017.xlsx', 'oct2017.xlsx', 'nov2017.xlsx', 'dec2017.xlsx',
         'jan2018.xlsx', 'feb2018.xlsx', 'mar2018.xlsx', 'apr2018.xlsx']


def read_files():
    print("Reading TTC data and calculating subway delays...")
    for file in files:
        # Load spreadsheet
        file_name = "../Resources/" + file
        xl = pd.ExcelFile(file_name)
        df1 = xl.parse(xl.sheet_names[0])

        delay = df1.groupby('Station')['Min Delay'].sum().reset_index()
        total_delay = delay.sort_values('Min Delay', ascending=False)
        dict_of_delays = total_delay.set_index('Station').T.to_dict('list')
        modified_dict = {key: sum(dict_of_delays[key]) for key in dict_of_delays}

        global subway_delays
        if not subway_delays:
            subway_delays = modified_dict.copy()
        else:
            for key in subway_delays.keys():
                try:
                    subway_delays[key] = subway_delays[key] + modified_dict[key]
                except:
                    pass


def clean_data():
    print("Cleaning the data....")
    # Remove subway yards and bus garages
    subway_delays.pop('WILSON HOSTLER', None)
    subway_delays.pop('KENNEDY PLATFORM 1', None)


def sort_subway_delay():
    sorted_subway_delays = sorted(subway_delays.items(),
                                  key=operator.itemgetter(1), reverse=True)
    return sorted_subway_delays


def write_to_file():
    print("Writing delay data to file...")
    with open('../Resources/subway_delays.txt', 'w') as file:
        file.write(json.dumps(sort_subway_delay()))

read_files()
clean_data()
write_to_file()

