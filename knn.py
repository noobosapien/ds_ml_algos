#Mary feels cold when it is 10C and warm when it is 25C
#If the room temperature is 22C the KNN will guess she feels warm
import sys
import math
import common.sort as sort
import common.common as common

def euclidean_distance(*args):
    x1, x2, y1, y2 = args
    return math.sqrt((x1 - x2)* (x1 - x2) + (y1 - y2)* (y1 - y2))

def manhattan_2d(*args):
    x1, x2, y1, y2 = args
    return abs(x1 - x2) + abs(y1 - y2)

# reset the count for neighbors and the groups of a data point
def info_reset(info):
    info["nbhd_count"] = 0
    info["class_count"] = {}

# find the group of neighbor with x and y
# if the class is known count that neighbor
# info contains information from the data provided
def info_add(info, data,x, y):
    group = data.get((x, y), None)
    common.dic_inc(info['class_count'], group)
    info['nbhd_count'] += int(group is not None)

# KNN algorithm to the 2D dataset with Manhattan distance
# the data dictionary has the 2D coordinates and the values being class(group)
# x,y are integer coordinates for the 2D data with the range
# [x_from,x_to] * [y_from,y_to]
def knn_to_2d_data(data, x_from, x_to, y_from, y_to, k):
    pass