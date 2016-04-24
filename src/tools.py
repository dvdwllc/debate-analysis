import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.rcParams.update({'font.size': 22})
matplotlib.rc('xtick', labelsize=22)
matplotlib.rc('ytick', labelsize=22)

spectrum = pd.read_csv('txt/huffpo_spectrum.txt',
                       names=['firstname','lastname','rating'])

def lower2(s):
    return s.lower()


def plot_ideology(ideology, title='prediction'):
    """
    plots predicted ideology on a -10 to 10 scale along with the values of
    several politicians for reference.
    """

    # candidates and ratings to plot
    bignames = ('Your text', 'Sanders', 'Clinton',
                'Christie', 'Trump', 'Rubio', 'Cruz')
    ratings = [
        spectrum[spectrum['lastname'] == i]['rating'].values[0]
        for i in bignames[1:]
        ]
    y_pos = np.arange(len(bignames))+2

    cm = plt.get_cmap('RdBu')  # colormap

    [plt.barh(a, b, align='center', color=cm(1 - (b + 10) / 20.), alpha=0.4)
     for (a, b) in zip(y_pos[1:], ratings)]

    plt.barh(y_pos[0], ideology,
             align='center', color=cm(1 - (ideology + 10) / 20.), alpha=0.8)
    plt.yticks(y_pos, bignames)
    plt.axis([-10, 10, 1, 10])
    plt.text(-6.5, 9, 'LIBERAL', color=cm(0.99))
    plt.text(1.8, 9, 'CONSERVATIVE', color=cm(0.01))
    plt.fill_between([-10, 10], [2.5, 2.5], [1.5, 1.5], color='black', alpha=0.2)
    plt.plot([0, 0], [0, 10], '-', color='black')
    plt.xticks([])
    plt.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.01)
    plt.savefig('static/img/%s.png' % title, transparent=True)
    plt.clf()
