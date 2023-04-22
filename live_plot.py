import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd


STEPS_SHOWN = 1000
length_csv_file = 0

plt.style.use('fivethirtyeight')
plt.tight_layout()

def animate(i):
    global length_csv_file
    to_skip_rows = length_csv_file - STEPS_SHOWN if length_csv_file - STEPS_SHOWN >= 0 else 0
    data = pd.read_csv('data.csv', skiprows=lambda x: x < to_skip_rows and x != 0)
    length_csv_file = len(data['time'])
    x = data['time'].iloc[-STEPS_SHOWN:]
    y = data['measurement'].iloc[-STEPS_SHOWN:]
    yf = data['filtered_measurement'].iloc[-STEPS_SHOWN:]

    plt.cla()
    plt.plot(x, y, label='rpm', linewidth=2)
    plt.plot(x, yf, label='filtered rpm', linewidth=2)
    # plt.xlim([0, 1000])
    # plt.ylim([0, 300])
    plt.legend(loc='upper left')
    plt.tight_layout()


animation = FuncAnimation(plt.gcf(), animate, interval=5,  cache_frame_data=True)
plt.show()
