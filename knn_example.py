import sys
sys.path.append('./common_utils')
import common_utils.common_utils as common_utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
# matplotlib.style.use('ggplot')

file_name = 'knn_example.data'
temp_from = 5
temp_to = 30
wind_from = 0
wind_to = 10

data = np.loadtxt(open(file_name, 'r'), dtype={'names': ('temperature', 'wind', 'perception'), 'formats': ('i4', 'i4', 'S4')})

for i in range(0, len(data)):
    if data[i][2] == 'cold:':
        data[i][2] = 'blue'
    elif data[i][2] == 'warm':
        data[i][2] =  'red'
    else:
        data[i][2] = 'gray'

data_processed = common_utils.get_x_y_colors(data)

plt.title('Temperature preferences')
plt.xlabel('Temperature in C')
plt.ylabel('Wind speed in kmph')
plt.axis((temp_from, temp_to, wind_from, wind_to))

blue_path = mpatches.Patch(color='blue', label='cold')
red_path = mpatches.Patch(color='red', label='warm')
plt.legend(handles=[blue_path, red_path])
plt.scatter(data_processed['x'], data_processed['y'], c=data_processed['colors'], s=[1400] * len(data))
plt.show()