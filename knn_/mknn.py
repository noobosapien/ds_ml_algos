import sys

sys.path.append("./common_utils")
import common_utils.common_utils as common
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

data_file = sys.path[0] + "/mknn.data"
temp_from = 5
temp_to = 30
wind_from = 0
wind_to = 10

data = np.loadtxt(
    open(data_file, "r"),
    dtype={
        "names": ("temperature", "wind", "perception"),
        "formats": ("i4", "i4", "S4"),
    },
)

# Convert classes to the colors to be displayed in the diagram
for i in range(0, len(data)):
    if data[i][2] == b"cold":
        data[i][2] = "blue"
    elif data[i][2] == b"warm":
        data[i][2] = "red"
    else:
        data[i][2] = "gray"

data_processed = common.get_x_y_colors(data)

plt.title("Mary and temperature preferences")
plt.xlabel("Temperature in C")
plt.ylabel("Wind speed in kmph")
plt.axis([temp_from, temp_to, wind_from, wind_to])

blue_patch = mpatches.Patch(color="blue", label="cold")
red_patch = mpatches.Patch(color="red", label="warm")

plt.legend(handles=[blue_patch, red_patch])

for i in range(len(data_processed["colors"])):
    if data_processed["colors"][i] == b"red":
        data_processed["colors"][i] = (0.8, 0.2, 0.2)
    elif data_processed["colors"][i] == b"blue":
        data_processed["colors"][i] = (0.2, 0.2, 0.8)
    else:
        data_processed["colors"][i] = (0.5, 0.5, 0.5)

plt.scatter(
    data_processed["x"],
    data_processed["y"],
    c=data_processed["colors"],
    s=[1400] * len(data),
)

plt.show()
