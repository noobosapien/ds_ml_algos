import sys

sys.path.append("./common_utils")
import common_utils.common_utils as common
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
# matplotlib.style.use('ggplot')

file_name = sys.path[0] + "/knn_example.data"
temp_from = 5
temp_to = 30
wind_from = 0
wind_to = 10

data = np.loadtxt(
    open(file_name, "r"),
    dtype={
        "names": ("temperature", "wind", "perception"),
        "formats": ("i4", "i4", "S4"),
    },
)

for i in range(0, len(data)):
    if data[i][2] == "cold:":
        data[i][2] = "blue"
    elif data[i][2] == "warm":
        data[i][2] = "red"
    else:
        data[i][2] = "gray"

data_processed = common.get_x_y_colors(data)

plt.title("Temperature preferences")
plt.xlabel("Temperature in C")
plt.ylabel("Wind speed in kmph")
plt.axis((temp_from, temp_to, wind_from, wind_to))

blue_path = mpatches.Patch(color="blue", label="cold")
red_path = mpatches.Patch(color="red", label="warm")
plt.legend(handles=[blue_path, red_path])
print(data_processed)
plt.scatter(
    data_processed["x"],
    data_processed["y"],
    s=[1400] * len(data),
)
plt.show()
