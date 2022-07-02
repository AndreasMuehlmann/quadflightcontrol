import matplotlib
import matplotlib.pyplot as plt


def plot_learning_curve(x_axis, scores, figure_file):
    plt.plot(x_axis, scores)
    plt.savefig(figure_file)
