# Mary feels cold when it is 10C and warm when it is 25C
# If the room temperature is 22C the KNN will guess she feels warm
import sys
import math

sys.path.append("./common_utils")
import common_utils.sort as sort
import common_utils.common_utils as common


def euclidean_distance(*args):
    x1, x2, y1, y2 = args
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


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
def info_add(info, data, x, y):
    group = data.get((x, y), None)
    common.dic_inc(info["class_count"], group)
    info["nbhd_count"] += int(group is not None)


# KNN algorithm to the 2D dataset with Manhattan distance
# the data dictionary has the 2D coordinates and the values being class(group)
# x,y are integer coordinates for the 2D data with the range
# [x_from,x_to] * [y_from,y_to]
def knn_to_2d_data(data, x_from, x_to, y_from, y_to, k):
    new_data = {}
    info = {}

    # Go through every point
    for y in range(y_from, y_to + 1):
        for x in range(x_from, x_to + 1):
            info_reset(info)

            # count all neighbors for each group of class
            # every distance dist starting at 0 until at least k
            # neighbors with known classes are found.
            for dist in range(0, x_to - x_from + y_to - y_from):
                # count all neighbors that are distanced dist from the point [x, y]
                if dist == 0:
                    info_add(info, data, x, y)
                else:
                    for i in range(0, dist + 1):
                        info_add(info, data, x - i, y + dist - i)
                        info_add(info, data, x + dist - i, y - i)
                    for i in range(1, dist):
                        info_add(info, data, x + i, y + dist - i)
                        info_add(info, data, x - dist + i, y - i)

                # There could be more than k-closest neighbors if the
                # distance of more of them is the same from the point
                # [x, y], but immediatly when we have at least k of
                # them, break from the loop.
                if info["nbhd_count"] >= k:
                    break

            class_max_count = None

            # choose the class with the highest count of the closest
            # neigbors
            for group, count in info["class_count"].items():
                if group is not None and (
                    class_max_count is None
                    or count > info["class_count"][class_max_count]
                ):
                    class_max_count = group
            new_data[x, y] = class_max_count

    return new_data


# Distance Buffer - keeping the calculated distances in a sorted order


class DistanceBuffer:
    def __init__(self, metric):
        self.metric = metric
        self.dist_list = [(0, 0, 0)]
        self.pos = 0
        self.max_covered_dist = 0

    def reset(self):
        self.pos = 0

    def next(self):
        if self.pos < len(self.dist_list):
            (x, y, dist) = self.dist_list[self.pos]
            if dist <= self.max_covered_dist:
                self.pos += 1
                return (x, y)

        self.__loadNext()
        return self.next()

    # Loads mor items into the buffer so that more of them are
    # available for the next() method

    def __loadNext(self):
        self.max_covered_dist += 1
        for x in range(-self.max_covered_dist, self.max_covered_dist + 1):
            self.__append(x, -self.max_covered_dist)
            self.__append(x, self.max_covered_dist)
        for y in range(-self.max_covered_dist + 1, self.max_covered_dist):
            self.__append(-self.max_covered_dist, y)
            self.__append(self.max_covered_dist, y)
        self.__sortList()

    def __append(self, x, y):
        self.dist_list.append((x, y, self.metric((0, 0), (x, y))))

    # Assuming that the sorting algorithm does not change the order of the
    # initial already sorted elements. This is so that next() does not skip
    # some elements and returns a different element instead
    def __sortList(self):
        self.dist_list.sort(key=proj_to_3rd)

    def printList(self):
        print(self.dist_list)


def proj_to_3rd(*args):
    d = args
    return d


def less_than_on_3rd(*args):
    (x1, y1, d1), (x2, y2, d2) = args
    return d1 < d2


def knn_to_2d_data_with_metric(
    data,
    x_from,
    x_to,
    y_from,
    y_to,
    k,
    lookup_limit,
    default,
    metric=manhattan_2d,
):
    new_data = {}
    info = {}
    db = DistanceBuffer(metric)

    # Go through every point in an integer coordinate system

    for y in range(y_from, y_to + 1):
        for x in range(x_from, x_to + 1):
            info_reset(info)
            db.reset()

            # Count the number of neighbors for each class group for
            # every distance dist starting at 0 until at least k
            # neighbors with known classes are found

            lookup_count = 0
            while info["nbhd_count"] < k and lookup_count < lookup_limit:
                (x0, y0) = db.next()
                xn = x + x0
                yn = y + y0

                if x_from <= xn and xn <= x_to and y_from <= yn and yn <= y_to:
                    info_add(info, data, xn, yn)

                lookup_count += 1

            # Choose the class with the highest count of the neighbors
            # from among the k-closest neighbors.
            result = common.dic_key_max_count(info["class_count"])
            if result is None:
                new_data[x, y] = default
            else:
                new_data[x, y] = result

    return new_data
