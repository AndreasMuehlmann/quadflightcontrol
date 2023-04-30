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
    time = data['time'].iloc[-STEPS_SHOWN:]
#   r1= data['r1'].iloc[-STEPS_SHOWN:]
#   r2= data['r2'].iloc[-STEPS_SHOWN:]
#   r3= data['r3'].iloc[-STEPS_SHOWN:]
#   r4= data['r3'].iloc[-STEPS_SHOWN:]
#   fr1= data['fr1'].iloc[-STEPS_SHOWN:]
#   fr2= data['fr2'].iloc[-STEPS_SHOWN:]
#   fr3= data['fr3'].iloc[-STEPS_SHOWN:]
#   fr4= data['fr4'].iloc[-STEPS_SHOWN:]
    # rotation= data['rotation'].iloc[-STEPS_SHOWN:]
    frotation= data['frotation'].iloc[-STEPS_SHOWN:]
    height_vel = data['height_vel'].iloc[-STEPS_SHOWN:]
    fheight_vel= data['fheight_vel'].iloc[-STEPS_SHOWN:]
#   o1= data['o1'].iloc[-STEPS_SHOWN:]
#   o2= data['o2'].iloc[-STEPS_SHOWN:]
#   o3= data['o3'].iloc[-STEPS_SHOWN:]
#   o4 = data['o4'].iloc[-STEPS_SHOWN:]

    plt.cla()
#   plt.plot(time, r1, label='r1', linewidth=2)
#   plt.plot(time, r2, label='r2', linewidth=2)
#   plt.plot(time, r3, label='r3', linewidth=2)
#   plt.plot(time, r4, label='r4', linewidth=2)
#   plt.plot(time, fr1, label='fr1', linewidth=2)
#   plt.plot(time, fr2, label='fr2', linewidth=2)
#   plt.plot(time, fr3, label='fr3', linewidth=2)
#   plt.plot(time, fr4, label='fr4', linewidth=2)
    # plt.plot(time, rotation, label='rotation', linewidth=2)
    plt.plot(time, frotation, label='frotation', linewidth=2)
    plt.plot(time, height_vel, label='height_vel', linewidth=2)
    plt.plot(time, fheight_vel, label='fheight_vel', linewidth=2)
#   plt.plot(time, o1, label='o1', linewidth=2)
#   plt.plot(time, o2, label='o2', linewidth=2)
#   plt.plot(time, o3, label='o3', linewidth=2)
#   plt.plot(time, o4, label='o4', linewidth=2)
    plt.legend(loc='upper left')
    plt.tight_layout()


animation = FuncAnimation(plt.gcf(), animate, interval=5,  cache_frame_data=True)
plt.show()
