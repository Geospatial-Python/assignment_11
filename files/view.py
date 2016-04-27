import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import QtCore
from PyQt4 import QtWidgets

from . import io_geojson
from . import twitter
import folium
import random
from .analytics import average_nearest_neighbor_distance
from .point_pattern import compute_g
from .point_pattern import average_nearest_neighbor_distance_numpy

class View(QtGui.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        self.map = None
        self.web_view = None
        map_osm.save('/tmp/map.html')
        self.init_ui

    def init_ui(self):
        #central widget
        self.web_view = QtWebkit.QWebView()
        self.map = folium.Map(location=[33.4484, -112.0740])
        self.map.zoom_start = 10
        self.map.save(r"./index.html")
        self.web_view.load
        self.setCentralWidget(self.web_view)

        #Open actions
        open_action = QtGui.QAction(QtGui.QIcon('Open_Folder.ico'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open)
        
        #Exit actions
        exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        positive_action = QtGui.QAction('Positive Tweets', self)
        positive_action.setStatusTip('Click to View Positive Tweets')
        positive_action.triggered.connect(self.display_positive)

        negative_action = QtGui('Negative Tweets', self)
        negative_action.setStatusTip('Click to View Negative Tweets')
        negative_action.triggered.connect(self.display_negative)

        neutral_action = QtGui('Neutral Tweets', self)
        neutral_action.setStatusTip('Click to View Neutral Tweets')
        neutral_action.triggered.connect(self.display_neutral)

        #Nearest Neighbor of Tweets
        nearest_neighbor_tweet = QtGui.QAction('Average Nearest Neighbor Distance')
        nearest_neighbor_tweet.setStatusTip('Calculate Nearest Neighbor Distance')
        nearest_neighbor_tweet.triggered.connect(self.display_nearest_neighbor_tweet)

        #G Function
        g_function_action = QtGui.QAction('G Function')
        g_function_action.setStatusTip('Calculate G Function')
        g_function_action.triggered.connect(self.display_g_function_action)


        #Menu Bar with visualize and calculate
        menu_bar = self.menuBar()

        menu_file = menu_bar.addMenu('&File')
        menu_file.addAction(exit_action)
        menu_file.AddAction(open_action)

        toolbar = self.addToolBar('Quit')
        toolbar.addAction(exit_action)
        toolbar = self.addAction('Open Json File')
        toolbar.addAction(open_action)
        toolbar = self.addToolbar('Positive Tweets')
        toolbar.addAction(positive_action)
        toolbar = self.addToolBar('Negative Tweets')
        toolbar.addAction(negative_action)
        toolbar = self.addToolBar('Neutral Tweets')
        toolbar.addAction(neutral_action)


        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Title Window')
        self.show()


    def map_tweets(self):
        file_name = QFileDialog.getOpenFileName(self, caption='Open File', directory='', filter='*.json')
        if not file_name:
            return
    
        tweets = io_geojson.read_twitter(file_name):
        for t in tweets:
            map_data = twitter.Tweet(t)
            folium.Marker([map_data.bounds[0][1], map_data.bounds[0][0]], popup = map_data).add_to(self.map)
            tweets.append(twitter.Tweet(t))

        self.map.save(r"./index.html")
        self.webView.setHtml(open("./index.html").read())
        self.webView.show()


    def positive_tweets(self, tweets):
        self.map = folium.Map(location=[33.4484, -112.0740])

        for t in tweets:
            print(t.sentiment)
            if t.sentiment == 'Positive':
                folium.Marker([t.bounds[0][1], t.bounds[0][0]], popup = t.text).add_to(self.map)

        self.map.save(r"./index.html")
        self.webView.setHtml(open("./index.html").read())
        self.webView.show()

    def negative_tweets(self, tweets):
        self.map = folium.Map(location=[33.4484, -112.0740])

        for t in tweets:
            print(t.sentiment)
            if t.sentiment == 'Negative':
                folium.Marker([t.bounds[0][1], t.bounds[0][0]], popup = t.text).add_to(self.map)

        self.map.save(r"./index.html")
        self.webView.setHtml(open("./index.html").read())
        self.webView.show()

    def neutral_tweets(self, tweets):
        self.map = folium.Map(location=[33.4484, -112.0740])

        for t in tweets:
            print(t.sentiment)
            if t.sentiment == 'Neutral':
                folium.Marker([t.bounds[0][1], t.bounds[0][0]], popup = t.text).add_to(self.map)

        self.map.save(r"./index.html")
        self.webView.setHtml(open("./index.html").read())
        self.webView.show()

    def display_avg_nearest_neighbor(self):

        icon = QtGui.QMessageBox()
        icon.setIcon(QtGui.QMessageBox.Information)
        text = "Average Nearest Neighbor Distance: " + str(average_nearest_neighbor_distance_numpy(self.tweets))
        print(text)
        icon.setText(text)
        icon.setWindowTitle("Average Nearest Neighbor Distance")
        icon.exec()

    def compute_g_tweets(self):


def main():
    app = QtGui.QApplication(sys.argv)
    view = View()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
