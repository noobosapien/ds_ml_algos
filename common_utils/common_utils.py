import random
import csv
import sys


def dic_inc(dic, key):
    if key is None:
        pass
    if dic.get(key, None) is None:
        dic[key] = 1
    else:
        dic[key] = dic[key] + 1


# returns a dictionary key with the max_count
def dic_key_max_count(dic):
    key_max_count = None
    for key, count in dic.items():
        if key is not None and (key_max_count is None or count > dic[key_max_count]):
            key_max_count = key
    return key_max_count


def get_x_y_colors(data):
    dic = {}
    dic["x"] = [0] * len(data)
    dic["y"] = [0] * len(data)
    dic["colors"] = [0] * len(data)

    for i in range(0, len(data)):
        dic["x"][i] = data[i][0]
        dic["y"][i] = data[i][1]
        dic["colors"][i] = data[i][2]
    return dic


def load_3row_data_to_dic(input_file):
    f = open(input_file, "r")
    dic = {}
    entries = (f.read()).splitlines()
    for i in range(0, len(entries)):
        values = entries[i].split(" ")
        dic[int(values[0]), int(values[1])] = values[2]
    return dic


def save_3row_data_to_file(output_file, data):
    f = open(output_file, "w")
    for key, value in data.items():
        f.write(str(key[0]) + " " + str(key[1]) + " " + value + "\n")


def dic_key_count(dic, key):
    if key is None:
        return 0
    if dic.get(key, None) is None:
        return 0
    else:
        return int(dic[key])


def csv_file_to_ordered_data(file_name):
    data = csv_file_to_list(file_name)
    return order_csv_data(data)


def order_csv_data(data):
    heading = data.pop(0)
    complete_data = []
    incomplete_data = []

    enquired_column = len(heading) - 1

    for data_item in data:
        if is_complete(data_item, enquired_column):
            complete_data.append(data_item)
        else:
            incomplete_data.append(data_item)
    return (heading, complete_data, incomplete_data, enquired_column)


def is_complete(data_item, pos):
    return data_item[pos] != "?"


def csv_file_to_list(csv_file_name):
    with open(csv_file_name, "r") as f:
        reader = csv.reader(f)
        data = list(reader)

    return data
