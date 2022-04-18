import numpy as np
import matplotlib.pyplot as plt

def init_changing_plot():
    plt.ion()
    plt.show()
    plt.xlabel('episode')
    plt.ylabel('score')
    plt.plot([], [])
    plt.draw()
    plt.pause(0.001)

def draw_plot(episode, avg_scores):
    plt.plot([j + 1 for j in range(episode + 1)], avg_scores)
    plt.draw()
    plt.pause(0.002)

def plot_learning_curve(x, scores, figure_file):
    running_avg = np.zeros(len(scores))
    for i in range(len(running_avg)):
        running_avg[i] = np.mean(scores[max(0, i-100):(i+1)])
    plt.plot(x, running_avg)
    plt.title('Running average of previous 100 scores')
    plt.savefig(figure_file)