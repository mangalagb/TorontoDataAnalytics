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


def clean_data_and_write_to_file():
    print("Cleaning the data....")
    # Remove subway yards and bus garages
    values_to_remove = {"WILSON HOSTLER", "KENNEDY PLATFORM 1", "KENNEDY BD STATION"}
    subway_details = {}

    for key, value in subway_delays.items():
        value_flag = True

        for invalid_value in values_to_remove:
            if invalid_value in key:
                value_flag = False

        if value_flag and value is not 0:
            name = key.split("(", 1)[0]
            if name not in subway_details:
                subway_details[name] = value
            else:
                subway_details[name] += value

    # Replace with the clean version
    subway_delays.clear()
    write_to_file(subway_details)


def sort_subway_delay(subway_details):
    sorted_subway_delays = sorted(subway_details.items(),
                                  key=operator.itemgetter(1), reverse=True)
    return sorted_subway_delays


def write_to_file(subway_details):
    print("Writing delay data to file...")
    with open('../Resources/subway_delays.txt', 'w') as file:
        file.write(json.dumps(sort_subway_delay(subway_details)))

read_files()
clean_data_and_write_to_file()
print("All Done!!")
