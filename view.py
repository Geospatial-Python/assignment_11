from PyQt5 import QtCore, QtWidgets, QtWebKitWidgets
from analytics import average_nearest_neighbor_distance
from utils import g_function
from tkinter import Tk
import tkinter.messagebox as mb
import sys
import folium
import io_geojson
import Tweet
import random
import matplotlib.pyplot as plt

PHX_COORDS = [33.441957, -112.072913]
NORMALIZED_PHX_DISTANCE = 57.68
AVG_DIST_ALL = 4.293
AVG_DIST_POS = 9.113
AVG_DIST_NEG = 11.12
AVG_DIST_NEU = 5.367

class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(434, 316)

        self.map = folium.Map(location=PHX_COORDS)
        self.map.zoom_start = 8
        self.mapFile = "osm_map.html"
        self.map.save(self.mapFile)
        self.sentiment = None

        self.setupUi()

    def setupUi(self):

        self.setupMenuBar()
        self.setupStatusBar()


        # place widgets here
        self.webView = QtWebKitWidgets.QWebView(MainWindow)
        self.webView.setHtml(open(self.mapFile,'r').read())



        self.MainWindow.setCentralWidget(self.webView)

    def setupMenuBar(self):

        # Exit
        exitAction = QtWidgets.QAction(self.MainWindow)
        exitAction.setText('Exit')
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        # Open
        openAction = QtWidgets.QAction(self.MainWindow)
        openAction.setText('Open')
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a tweet .json file')
        openAction.triggered.connect(lambda x: self.visualizeTweets("All"))

        # Positive tweets
        posTwAction = QtWidgets.QAction(self.MainWindow)
        posTwAction.setText('Positive Tweets')
        posTwAction.setStatusTip('Remap tweet locations based on Positive senitmental tweets')
        posTwAction.triggered.connect(lambda x: self.visualizeTweets('Positive'))

        # Negative tweets
        negTwAction = QtWidgets.QAction(self.MainWindow)
        negTwAction.setText('Negative Tweets')
        negTwAction.setStatusTip('Remap tweet locations based on negative senitmental tweets')
        negTwAction.triggered.connect(lambda x: self.visualizeTweets('Negative'))

        # Neutral tweets
        neuTwAction = QtWidgets.QAction(self.MainWindow)
        neuTwAction.setText('Neutral Tweets')
        neuTwAction.setStatusTip('Remap tweet locations based on neutral senitmental tweets')
        neuTwAction.triggered.connect(lambda x: self.visualizeTweets('Neutral'))

        # Compute Nearest Neighbor of Tweets
        nnTwAction = QtWidgets.QAction(self.MainWindow)
        nnTwAction.setText('Nearest Neighbor')
        nnTwAction.setStatusTip('Find nearest neighbor of tweets')
        nnTwAction.triggered.connect(self.nearestNeighborTweets)

        # Compute G function
        gfTwAction = QtWidgets.QAction(self.MainWindow)
        gfTwAction.setText('G Function')
        gfTwAction.setStatusTip('Compute the G function on tweets')
        gfTwAction.triggered.connect(self.compGFunction)

        menubar = QtWidgets.QMenuBar(self.MainWindow)

        menuFile = QtWidgets.QMenu(menubar)
        menuFile.setTitle('File')
        menuFile.addAction(exitAction)
        menuFile.addAction(openAction)

        menuVisu = QtWidgets.QMenu(menubar)
        menuVisu.setTitle('Visualize')
        menuVisu.addAction(posTwAction)
        menuVisu.addAction(negTwAction)
        menuVisu.addAction(neuTwAction)

        menuComp = QtWidgets.QMenu(menubar)
        menuComp.setTitle('Compute')
        menuComp.addAction(nnTwAction)
        menuComp.addAction(gfTwAction)


        self.MainWindow.setMenuBar(menubar)


        menubar.addAction(menuFile.menuAction())
        menubar.addAction(menuVisu.menuAction())
        menubar.addAction(menuComp.menuAction())

    def setupStatusBar(self):
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.MainWindow.setStatusBar(self.statusbar)

    def visualizeTweets(self, sentiment):
        self.sentiment = sentiment
        jfile = self.openJFile()
        self.tweetObjArr = self.filterTweets(self.processTweetFile(jfile))
        self.mapTweets(self.tweetObjArr)

    def nearestNeighborTweets(self):
        """ In this function, I will normalize it to the unit mile
        by multiplying the result by the distance in miles traveling
        about 1 unit longitudinally at roughly the same latitude.
        first coord = (33.471798, -112.445462)
        second coord = (33.451355, -111.442852)
        Distance (Miles / Spherical Earth) = 57.68 miles
        """
        root = Tk()
        root.withdraw()
        if self.sentiment == None:
            mb.showerror("Error", 'Please Open or Visualize tweets first.')
        else:
            if self.sentiment == 'All':
                mark = None
            else:
                mark = self.sentiment
            nnd = NORMALIZED_PHX_DISTANCE * average_nearest_neighbor_distance(self.tweetObjArr, mark)
            mb.showinfo("Info", 'The average nearest neighbor of\n{0} tweets is {1}'.format(self.sentiment, nnd))

        # Result for All Tweets = 4.293
        # Result for Positive Tweets = 9.113
        # Result for Negative Tweets = 11.12
        # Result for Neutral Tweets = 5.367

    def compGFunction(self):
        root = Tk()
        root.withdraw()
        if self.sentiment == None:
            mb.showerror("Error", 'Please Open or Visualize tweets first.')
        else:
            pointsArr = []
            for tw in self.tweetObjArr:
                pointsArr.append(tw.getPoint())

            samples = 200
            d = []
            G_d = []
            if self.sentiment == 'All':
                for x in range(0, samples):
                    i = AVG_DIST_ALL / samples * x
                    d.append(i)
                    G_d.append(g_function(pointsArr, i))
            elif self.sentiment == 'Positive':
                for x in range(0, samples):
                    i = AVG_DIST_POS / samples * x
                    d.append(i)
                    G_d.append(g_function(pointsArr, i))
            elif self.sentiment == 'Negative':
                for x in range(0, samples):
                    i = AVG_DIST_NEG / samples * x
                    d.append(i)
                    G_d.append(g_function(pointsArr, i))
            elif self.sentiment == 'Neutral':
                for x in range(0, samples):
                    i = AVG_DIST_NEU / samples * x
                    d.append(i)
                    G_d.append(g_function(pointsArr, i))

            plt.figure(1)
            plt.plot(d, G_d, 'bo')
            plt.title('G function of {} tweets.'.format(self.sentiment))
            plt.xlabel('Distance d (miles)')
            plt.ylabel('G(d)')
            plt.show()

    def openJFile(self):
        try:
            jfile = QtWidgets.QFileDialog.getOpenFileName(parent=MainWindow, caption='Open a tweet .json file',filter='*.json')[0]
            return jfile
        except:
            root = Tk()
            root.withdraw()
            mb.showinfo("Error", 'Could not open tweet file.')

    def processTweetFile(self, jfile):
        tweetObjs = []
        tweets = io_geojson.processTweets(jfile)
        for t in tweets:
            tweetObjs.append(Tweet.Tweet(t))
        return tweetObjs


    def filterTweets(self, tweetObjs):
        filteredTweets = []
        for tw in tweetObjs:
            if self.sentiment == "All":
                filteredTweets.append(tw)
            elif tw.sentiment == self.sentiment:
                filteredTweets.append(tw)
        return filteredTweets


    def mapTweets(self, tweetObjs):

        random.seed(1212)

        # create new map for new file
        self.map = folium.Map(location=PHX_COORDS)
        self.map.zoom_start = 8

        for tw in tweetObjs:
            latitude, longitude = tw.getRandPointInBoundingBox()
            folium.Marker([latitude, longitude], popup=tw.twText).add_to(self.map)

        self.map.save(self.mapFile)
        self.webView.setHtml(open(self.mapFile,'r', encoding="utf8").read())
        # used https://nlp.fi.muni.cz/projects/chared/ to find out encoding


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
