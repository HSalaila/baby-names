from flask import Flask, request, render_template
from src.pandashandler import *
import matplotlib.pyplot as plt
import numpy as np
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/analyse')
def analyse():
    d = request.args.to_dict()
    analysis = filter_two_names(read_csv(), d["name1"], d["name2"])
    generateplots(analysis.copy())
    # time used as cache buster - http://flask.pocoo.org/snippets/40/
    return render_template("result.html", result=analysis.items(), time=str(time.time()))


def generateplots(result):
    fig = plt.figure()
    # line plot
    for name, value in result.items():
        plt.plot(value, label=name)
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend()
    plt.savefig("static/lineplot")
    fig.clear()
    # scatter plot
    name1 = result.popitem()
    name2 = result.popitem()
    x = name1[1]
    y = name2[1]

    coeff = np.polyfit(x, y, 1)

    def correlation():
        # http://stackoverflow.com/questions/3425439/why-does-corrcoef-return-a-matrix
        return np.corrcoef(x, y)[0, 1]

    def plotbestfitline():
        # http://stackoverflow.com/questions/22239691/code-for-line-of-best-fit-of-a-scatter-plot-in-python
        plt.plot(x, np.poly1d(coeff)(x))

    plt.scatter(x, y)
    plotbestfitline()

    corr = correlation()
    slope = coeff[0]
    intercept = coeff[1]

    plt.title(name1[0] + " - " + name2[0] + "\n" +
              "Correlation: " + str(corr) + " slope: " + str(slope) + " intercept: " + str(intercept) + "\n")
    plt.savefig("static/scatterplot")
    plt.close()

if __name__ == '__main__':
    app.run()
