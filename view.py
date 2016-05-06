#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

This program creates a skeleton of
a classic GUI application with a menubar,
toolbar, statusbar and a central widget.

author: Jan Bodnar
website: zetcode.com
last edited: September 2011
"""

import sys
from PyQt4 import QtGui, QtWebKit, QtCore
import folium
import os
import src.tweet
import src.io_geojson
import src.point
import src.pointPattern
import matplotlib
import matplotlib.pyplot as pyp
import numpy as np



class View(QtGui.QMainWindow):

    def __init__(self):                 #calling the parent constructor
        super(View, self).__init__()

        self.initUI()
        self.positiveTweets = []
        self.negativeTweets = []
        self.neutralTweets = []
        self.allTweets = []
        self.loadedAlready = False
        self.currentlyPlotted = []
        self.tweetPattern = src.pointPattern.PointPattern()


    def initUI(self):

        self.resize(350,250)
        self.center()
        os.makedirs('temp',exist_ok=True) #for saving directory
        #textEdit = QtGui.QTextEdit()         #adding a QTextEdit as the central widget
        self.web_view = QtWebKit.QWebView()
        self.map_dir = 'temp/folium_map.html' #so it knows where to save

        #now embed the folium map
        #self.map = folium.Map(location=[-112.323914,-33.29026],zoom_start=10)
        self.map = folium.Map(location=[33.29026,-112.323914],zoom_start=10)
        self.map.save(self.map_dir)
        self.web_view.load(QtCore.QUrl(self.map_dir))

        self.setCentralWidget(self.web_view)

        #creates a toolbar to exit, along with adding a keyboard shortcut
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        openAction = QtGui.QAction('Open Tweets',self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Load tweets for marker display in map')
        openAction.triggered.connect(self.openAndDisplayMarkers)

        #add GUI menubar for all,pos,neg,neutral:
        positiveAction = QtGui.QAction('Positive Tweets',self)
        positiveAction.setStatusTip('Load only the positive sentiment tweets')
        positiveAction.triggered.connect(self.loadPositive) # change this

        negativeAction = QtGui.QAction('Negative Tweets',self)
        negativeAction.setStatusTip('Load only the negative sentiment tweets')
        negativeAction.triggered.connect(self.loadNegative)    #change this

        neutralAction = QtGui.QAction('Neutral Tweets',self)
        neutralAction.setStatusTip('Load only the neutral sentiment tweets')
        neutralAction.triggered.connect(self.loadNeutral) # change this

        allAction = QtGui.QAction('All Tweets',self)
        allAction.setStatusTip('Load all of the tweets')
        allAction.triggered.connect(self.loadAll) # change this

        avgNearNeighAction = QtGui.QAction('Average Nearest Neighbor',self)
        avgNearNeighAction.setStatusTip('Compute Average Nearest Neighbor Distance')
        avgNearNeighAction.triggered.connect(self.avgNN)

        gfuncAction = QtGui.QAction('G Function',self)
        gfuncAction.setStatusTip('Compute the g function of the points')
        gfuncAction.triggered.connect(self.gfuncCompute)

        #added a ready message to the status bar
        self.statusBar().showMessage('Ready')

        #creating the file menu, and adding exit as an option
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        #creating a toolbar with an exit function
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.addAction(openAction)
        toolbar.addAction(allAction)
        toolbar.addAction(positiveAction)
        toolbar.addAction(negativeAction)
        toolbar.addAction(neutralAction)
        toolbar.addAction(avgNearNeighAction)
        toolbar.addAction(gfuncAction)

        #setting the window name
        self.setWindowTitle('Tweet Map')
        self.show()

    def loadPositive(self):
        self.map = folium.Map(location=[33.29026,-112.323914],zoom_start=10)
        self.currentlyPlotted = self.positiveTweets
        self.markerRedraw(self.positiveTweets)

    def loadNegative(self):
        self.map = folium.Map(location=[33.29026,-112.323914],zoom_start=10)
        self.currentlyPlotted = self.negativeTweets
        self.markerRedraw(self.negativeTweets)

    def loadNeutral(self):
        self.map = folium.Map(location=[33.29026,-112.323914],zoom_start=10)
        self.currentlyPlotted = self.neutralTweets
        self.markerRedraw(self.negativeTweets)

    def loadAll(self):
        self.map = folium.Map(location=[33.29026,-112.323914],zoom_start=10)
        self.markerRedraw(self.allTweets)

    def avgNN(self):
        print("do stuff for avgNN")

    def gfuncCompute(self):
        #so here, you want to compute the g function on a set of points. Well, the points inside the twitter one are of a type Point.
        #tweet.geoPoint is of type point. So, you can use the list of tweets being visualized right now, then iterate through those
        #tweets, and add them as points to a point pattern... through I guess they are a point pattern.

        #so you have self.currentlyPlotted: [t1,t2,t3,t4], calculate the g function on that.
        for t in self.currentlyPlotted:
            self.tweetPattern.add_point(t.geoPoint)

        #now compute the g function:
        gfuncList,ds = self.tweetPattern.numpy_compute_g(12)

        #now plot it:






        fig2, ax2 = pyp.subplots()
        ax2.plot(np.array(ds),np.array(gfuncList),'ro-')
        ax2.set_xlabel(r'$d$')
        ax2.set_ylabel(r'$\hat{G}(d)$')
        ax2.set_title(r'$\hat{G}(d)$ Result')
        pyp.show()

    def markerRedraw(self,tweetsToDraw):
        #draw only the tweets in the list that are passed in:
        long_sum = 0
        lat_sum = 0
        for t1 in tweetsToDraw:
            markerPoint = [t1.latitude,t1.longitude]
            #now create the actual marker:
            markerToAdd = folium.Marker(markerPoint,popup= t1.tweetText)
            markerToAdd.add_to(self.map)

            #you need to recenter the map at the mean center of the points. That means that you have to calculate the mean center
            #as you go through all the points:
            long_sum = long_sum + markerPoint[0]
            lat_sum = lat_sum + markerPoint[1]

        mean_center_long = long_sum/len(tweetsToDraw)
        mean_center_lat = lat_sum/len(tweetsToDraw)
        mean_center = [mean_center_long,mean_center_lat]
            #now change the map location to there:
        self.map.location= mean_center

        self.map.save(self.map_dir)
        self.web_view.load(QtCore.QUrl(self.map_dir))

    #making it appear in the center of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openAndDisplayMarkers(self):
        print("openAndDisplayMarkers")
        file = QtGui.QFileDialog.getOpenFileName(self,caption='Open tweet file',filter='*.json') # for only json's
        if not file: #nothing selected, can't do anything
            return

        tweets = []
        j = 0
        tweet_dict = src.io_geojson.read_twitter_data(file)
        for t in tweet_dict: # for every tweet in the tweet dictionary
            if j < 10:
                tweets.append(src.tweet.Tweet(t))
                self.allTweets.append(src.tweet.Tweet(t))
                #now append them to a global list of all the pos/neg/neu tweets so that you can call them again later:
                temp = src.tweet.Tweet(t)
                if(temp.sentimentMark == 'Positive'):
                    self.positiveTweets.append(src.tweet.Tweet(t))
                elif(temp.sentimentMark == 'Negative'):
                    self.negativeTweets.append(src.tweet.Tweet(t))
                elif(temp.sentimentMark == 'Neutral'):
                    self.neutralTweets.append(src.tweet.Tweet(t))

            j = j +1
        #now that you've created an list of tweets implementing the Tweet class, use the saved
        #array to actually create the markers and get the latitude/longitude values from the points:
        long_sum = 0
        lat_sum = 0
        i = 0

        #set the currently visualized points:
        self.currentlyPlotted = tweets

        for t1 in tweets: #Going through each Tweet class element
            markerPoint = [t1.latitude,t1.longitude]
            if i < 5:
                print(markerPoint)
            #now create the actual marker:
            markerToAdd = folium.Marker(markerPoint,popup= t1.tweetText)
            markerToAdd.add_to(self.map)

            #you need to recenter the map at the mean center of the points. That means that you have to calculate the mean center
            #as you go through all the points:
            long_sum = long_sum + markerPoint[0]
            lat_sum = lat_sum + markerPoint[1]
            i = i + 1

        print(len(tweets))
        mean_center_long = long_sum/len(tweets)
        mean_center_lat = lat_sum/len(tweets)
        mean_center = [mean_center_long,mean_center_lat]
        #now change the map location to there:
        self.map.location= mean_center

        self.map.save(self.map_dir)
        self.web_view.load(QtCore.QUrl(self.map_dir))


def main():

    app = QtGui.QApplication(sys.argv)
    ex = View()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()