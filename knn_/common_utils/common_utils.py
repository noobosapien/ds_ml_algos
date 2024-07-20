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
        print(str(key[0]))
        f.write(str(key[0]) + " " + str(key[1]) + " " + value + "\n")
