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
    lineplot(analysis)
    scatterplot(analysis)
    # time used as cache buster - http://flask.pocoo.org/snippets/40/
    return render_template("result.html", result=analysis.items(), time=str(time.time()))


def lineplot(result):
    fig = plt.figure()
    for name, value in result.items():
        plt.plot(value, label=name)
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend()
    plt.savefig("static/lineplot")
    plt.close(fig)


def scatterplot(result):
    fig = plt.figure()
    tuple_values = [(name, value) for name, value in result.items()]
    x = tuple_values[0][1]
    y = tuple_values[1][1]

    plt.scatter(x, y)

    # http://stackoverflow.com/questions/3425439/why-does-corrcoef-return-a-matrix
    correlation = np.corrcoef(x, y)[0, 1]
    coefficient = np.polyfit(x, y, 1)

    # http://stackoverflow.com/questions/22239691/code-for-line-of-best-fit-of-a-scatter-plot-in-python
    plt.plot(x, np.poly1d(coefficient)(x))
    x_label = tuple_values[0][0]
    y_label = tuple_values[1][0]

    def format2d(value):
        return "{0:.2f}".format(value)
    stats = "Correlation: " + format2d(correlation) + \
            " Slope: " + format2d(coefficient[0]) + " Intercept: " + format2d(coefficient[1])
    fig.suptitle(x_label + " - " + y_label + "\n" + stats)
    plt.savefig("static/scatterplot")
    plt.close(fig)

if __name__ == '__main__':
    app.run()
