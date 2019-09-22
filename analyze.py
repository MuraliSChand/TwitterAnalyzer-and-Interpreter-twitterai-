import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pandas.plotting import register_matplotlib_converters
from practice import Practice
register_matplotlib_converters()


class Analyze:
    def __init__(self, filename):
        self.p = Practice(filename, False, False, False)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(131)
        self.ax2 = self.fig.add_subplot(132)
        self.ax3 = self.fig.add_subplot(133)
        self.words = []


        self.ax2.plot([0], [0])
        self.ax3.barh(['x'], [5])
        self.ax.plot([0], [0])

    def animate_sent(self, i):
        # global p
        # p = Practice("C:\\Users\\Murali Sai Chand\\PycharmProjects\\Twitterai\\tweets2.json")
        # p1 = get_obj()
        words = self.words
        x = self.p.sentiments(words)
        self.ax2.clear()
        for n, i in enumerate(x):
            xs1 = i.index
            ys1 = i.values
            self.ax2.plot(xs1, ys1, 'C' + str(n + 3), label=words[n])
        self.ax2.set_ylabel('Sentiment rate(per minute)')
        self.ax2.set_title("Sentiment Analyser.")
        self.ax2.legend()
        for i in self.ax2.get_xticklabels():
            i.set_rotation(90)
        self.fig.canvas.draw()

    def animate(self, i):
        # global p
        # p = Practice("C:\\Users\\Murali Sai Chand\\PycharmProjects\\Twitterai\\tweets2.json")
        # p1 = get_obj()
        self.p.reflat()
        dfs, names = self.p.finalize(self.words)
        self.ax.clear()
        for j, i in enumerate(dfs):
            x = i.index
            y = i.values
            self.ax.plot(x, y, label=names[j])
        self.ax.set_ylabel('Mean Tweets(per minute)')
        self.ax.set_title("Trends")
        self.ax.legend()
        for i in self.ax.get_xticklabels():
            i.set_rotation(90)
        self.fig.canvas.draw()

    def viz_top(self, i):
        # p = Practice("C:\\Users\\Murali Sai Chand\\PycharmProjects\\Twitterai\\tweets2.json")
        # p1 = get_obj()
        d = self.p.top_words()
        # set_obj()
        n = 0
        for i in d:
            n += i[1]
        x = [i[0] for i in d]
        y = [(i[1] / n) * 100 for i in d]
        self.ax3.clear()
        self.ax3.barh(x, y, color=[str(i / 100) for i in y])
        for i,v in enumerate(y):
            self.ax3.text(v,i,str(round(v,1))+"%")
        self.ax3.set_xlabel("Word Percentage")
        self.ax3.set_title("Top Words. Total tweets{}".format(self.p.n))
        plt.xticks(rotation=75)
        self.fig.canvas.draw()

    def show_viz(self, words = []):
        self.words = words
        ani2 = animation.FuncAnimation(self.fig, self.animate, interval=3000)
        ani = animation.FuncAnimation(self.fig, self.animate_sent, interval=3000)
        ani3 = animation.FuncAnimation(self.fig, self.viz_top, interval=3000)
        plt.show()

#ob = Analyze()
#ob.show_viz()

