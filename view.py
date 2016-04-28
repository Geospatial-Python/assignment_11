#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import folium
import io_geojson
from tweet import *
from point import *
from PyQt4 import QtGui, QtCore, QtWebKit
from  point_pattern import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import random
import time



class Window(QtGui.QDialog):
    def __init__(self, parent=None, data=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()
        self.data = data
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QtGui.QVBoxLayout()
        #layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        if self.data!=None:
            data = self.data
        else:
            data = [random.random() for i in range(10)]


        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(data[0],data[1], '*-')

        # refresh canvas
        self.canvas.draw()


class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        self.tweets = []
        self.current_data=[]
        
    def initUI(self):

        #self.webView = QtWebKit.QWebView()
        #first just show a map without marks in the map
        #the data is the last time i compute the averge of the lat/lon
        map_osm = folium.Map(location=[33.59359997467155,-111.94546800838894])
        map_osm.save(r"./map.html")

        self.webView = QtWebKit.QWebView()
        self.webView.setHtml(open(r"./map.html").read())
        self.setCentralWidget(self.webView)
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)



        positive = QtGui.QAction(QtGui.QIcon('positive.png'), 'show positive', self)
        positive.setStatusTip('Show positive Tweets')
        positive.triggered.connect(self.show_positive)

        negative = QtGui.QAction(QtGui.QIcon('negative.png'), 'show negative', self)
        negative.setStatusTip('Show negative Tweets')
        negative.triggered.connect(self.show_negative)

        neutral = QtGui.QAction(QtGui.QIcon('neutral.png'), 'show neutral', self)
        neutral.setStatusTip('Show neutral Tweets')
        neutral.triggered.connect(self.show_neutral)

        mean_dis = QtGui.QAction(QtGui.QIcon('mean_dis.png'), 'show mean_dis', self)
        mean_dis.setStatusTip('Show mean_dis ')
        mean_dis.triggered.connect(self.compute_mean_nearest_neighbor_distance)

        compute_g = QtGui.QAction(QtGui.QIcon('mean_dis.png'), 'show compute_g', self)
        compute_g.setStatusTip('Show compute_g ')
        compute_g.triggered.connect(self.show_compute_g)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(positive)
        fileMenu.addAction(negative)
        fileMenu.addAction(neutral) 
        fileMenu.addAction(mean_dis)
        fileMenu.addAction(compute_g)

        self.setGeometry(300, 300, 750, 650)
        self.setWindowTitle('WebView')
        self.show()
        self.webView.show()
        
    def showDialog(self):
        

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname == '':
            return 
        tweets=io_geojson.read_tweet_json(fname)

        tweets_data=[]
        for tweet_data in tweets:
            tweets_data.append(io_geojson.ingest_twitter_data(tweet_data))

        self.tweets = [Tweet(Point(tweet["point"][0],tweet["point"][1]),tweet["text"],tweet["source"],tweet["id_str"],tweet["lang"],tweet["created_time"]) for tweet in tweets_data]
        self.current_data = self.tweets 
        self.show_map_into_webview(self.current_data ,'All')

    def show_compute_g(self):

        points = [tweet.point for tweet in self.current_data]
        ppt = PointPattern(points)

        g = ppt.compute_g(len(points))

        
        self.main = Window(data=(len(points),g))
        self.main.show()

        
        

    def show_map_into_webview(self,tweets,flag):

        #compute the  mean center of the points.
        lat_all=[]
        lon_all=[]
        for tweet in tweets:
            lat_all.append(tweet.get_spatial_information()[0])
            lon_all.append(tweet.get_spatial_information()[1])

        avg_lat=sum(lat_all)/len(lat_all)
        avg_lon=sum(lon_all)/len(lon_all)

        #set a map with the avg_lat,avg_lon
        map_1 = folium.Map(location=[avg_lat, avg_lon])

        #set markers in the map
        for tweet in tweets:
            folium.Marker(list(tweet.get_spatial_information()), popup=tweet.text).add_to(map_1)

        if flag == 'All':
            html_path = r'./map.html'
        elif flag == 'Positive':
            html_path = r'./map_Positive.html'
        elif flag == 'Negative':
            html_path = r'./map_Negative.html'
        elif flag == 'Neutral':
            html_path = r'./map_Neutral.html'

        map_1.save(html_path)

        #set the webView with the map html
        self.webView.setHtml(open(html_path,encoding="utf-8").read())
        self.webView.show()

    def show_positive(self):

        self.current_data = [tweet for tweet in self.tweets if tweet.point.mark == 'Positive']

        self.show_map_into_webview(self.current_data ,'Positive')

    def show_negative(self):

        self.current_data = [ tweet for tweet in self.tweets if tweet.point.mark == 'Negative']

        self.show_map_into_webview(self.current_data ,'Negative')
        
        
    def show_neutral(self):

        self.current_data = [ tweet for tweet in self.tweets if tweet.point.mark == 'Neutral']

        self.show_map_into_webview(self.current_data,'Neutral')

    def compute_mean_nearest_neighbor_distance(self):

        points = [tweet.point for tweet in self.current_data]
        ppt = PointPattern(points)
        data = ppt.average_nearest_neighbor_distance()
        print("The mean_nearest_neighbor_distance of the visualized is: "+str(data))



def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
