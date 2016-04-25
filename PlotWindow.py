import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random


class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        #self.figure = plt.figure()

        self.fig, self.ax = plt.subplots()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.fig)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)



    def plot(self, x, y, label, color):
        ''' plot some random stuff '''
        # create an axis
        #ax = self.figure.add_subplot(111)

        # discards the old graph
        #ax.hold(False)

        # plot data
        self.ax.plot(x, y, label=label, color=color)

        # refresh canvas
        self.canvas.draw()

        self.ax.legend(loc=0)