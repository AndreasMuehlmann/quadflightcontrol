import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# tkinter has to be installed on the system (not through pip)
matplotlib.use('TkAgg')

def init_changing_plot():
    plt.ion()
    plt.show()
    plt.xlabel('episode')
    plt.ylabel('score')
    plt.plot([], [])
    plt.draw()
    plt.pause(3)

def draw_plot(x, ys):
    print(f'x: {x}, ys: {ys}')
    plt.plot([j + 1 for j in range(x)], ys)
    plt.draw()
    plt.pause(0.002)

def plot_learning_curve(x, scores, figure_file):
    running_avg = np.zeros(len(scores))
    for i in range(len(running_avg)):
        running_avg[i] = np.mean(scores[max(0, i-100):(i+1)])
    plt.plot(x, running_avg)
    plt.title('Running average of previous 100 scores')
    plt.savefig(figure_file)
