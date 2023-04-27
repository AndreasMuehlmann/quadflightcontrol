import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('fivethirtyeight')
plt.tight_layout()

data = pd.read_csv('data.csv')
time = data['time']
m = data['rotation']
fm = data['frotation']

plt.plot(time, m, label='m', linewidth=2)
plt.plot(time, fm, label='fm', linewidth=2)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
