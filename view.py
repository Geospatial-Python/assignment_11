import sys
from PyQt4 import QtGui, QtCore, QtWebKit
import folium
import io_geojson
import tweet
import point
import random
import matplotlib.pyplot as plt

class Example(QtGui.QMainWindow):
    
    
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        #textEdit = QtGui.QTextEdit()
        #self.setCentralWidget(textEdit)
        currentPoints = []
        positiveList = []
        negativeList = []
        neutralList = []
        activeList = 0
        
        map_osm = folium.Map(location=[33.59359997467155, -111.94546800838894])
        map_osm.save(r"./map.html")
        
        
        
        
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        
        showPositive = QtGui.QAction(QtGui.QIcon('pos.png'), 'Positive', self)
        showPositive.setShortcut('Ctrl+P')
        showPositive.setStatusTip('Show Positive Tweets')
        showPositive.triggered.connect(self.drawPositive)
        
        showNegative = QtGui.QAction(QtGui.QIcon('neg.png'), 'Negative', self)
        showNegative.setShortcut('Ctrl+N')
        showNegative.setStatusTip('Show Negative Tweets')
        showNegative.triggered.connect(self.drawNegative)
        
        showNeutral = QtGui.QAction(QtGui.QIcon('neutral.png'), 'Neutral', self)
        showNeutral.setShortcut('Ctrl+M')
        showNeutral.setStatusTip('Show Neutral Tweets')
        showNeutral.triggered.connect(self.drawNeutral)
        
        nearestNeighborDiag = QtGui.QAction(QtGui.QIcon('nn.png'), 'Nearest Neighbor', self)
        nearestNeighborDiag.setShortcut('Ctrl+B')
        nearestNeighborDiag.setStatusTip('Show Nearest Neighbor for current subset')
        nearestNeighborDiag.triggered.connect(self.drawNearest)
        
        computeGDiag = QtGui.QAction(QtGui.QIcon('compG.png'), 'Compute G', self)
        computeGDiag.setShortcut('Ctrl+G')
        computeGDiag.setStatusTip('Compute G for current subset')
        computeGDiag.triggered.connect(self.drawG)
        

        self.webView = QtWebKit.QWebView()
        self.webView.setHtml(open(r"./map.html").read())
        self.setCentralWidget(self.webView)
        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)    
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAction)
        fileMenu.addAction(showPositive)
        fileMenu.addAction(showNegative)
        fileMenu.addAction(showNeutral)
        fileMenu.addAction(nearestNeighborDiag)
        fileMenu.addAction(computeGDiag)
        

        toolbar = self.addToolBar('Open')
        toolbar.addAction(openFile)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar = self.addToolBar('Positive')
        toolbar.addAction(showPositive)
        toolbar = self.addToolBar('Negative')
        toolbar.addAction(showNegative)
        toolbar = self.addToolBar('Neutral')
        toolbar.addAction(showNeutral)
        toolbar = self.addToolBar('Nearest Neighbor')
        toolbar.addAction(nearestNeighborDiag)
        toolbar = self.addToolBar('Compute G')
        toolbar.addAction(computeGDiag)
        
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Assignment 11')    
        self.show()
        self.webView.show()

    def showDialog(self):
        global currentPoints
        global positiveList
        global negativeList
        global neutralList
        global activeList
        global map_1
        global average_lon
        global average_lat
        
        currentPoints = []
        positiveList = []
        negativeList = []
        neutralList = []
        
        
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname == '':
            return
        tweets=io_geojson.read_tweets(fname)
    
        tweets_data=[]
       # count = 0
        for i in tweets:
            tweets_data.append(tweet.Tweet(i))
           # count = count+1
            #if count==30:
             #   break

            
        average_lat = 0
        average_lon = 0
        count_tweets = 0
        
        random.seed(1234)
        
        
        
        
        for i in tweets_data:
            lat, lon = i.gen_point_in_bounds()
            currentPoints.append(point.Point(lat,lon,i.sentiment))
            
            if i.sentiment == 'Positive':
                positiveList.append(point.Point(lat,lon,i.sentiment))
            elif i.sentiment == 'Negative':
                negativeList.append(point.Point(lat,lon,i.sentiment))
            elif i.sentiment == 'Neutral':
                neutralList.append(point.Point(lat,lon,i.sentiment))
                
            
            average_lat += lat
            average_lon += lon
            count_tweets += 1
    
        average_lon /= len(tweets_data)
        average_lat /= len(tweets_data)
        map_1 = folium.Map(location=[average_lat, average_lon])
        
        #activeList = currentPoints
        
        #countttz = 0
        for i in currentPoints:
            #lat, lon = i.gen_point_in_bounds()
            lat = i.x
            lon = i.y
            sent = i.mark
            folium.Marker([lat, lon], popup = sent).add_to(map_1)
            
            #if countttz < 500:
                #print('Sup')
                #print(type(i.username))
           # print("hello")
            #print(i.sentiment)
                #print(type("Test"))
                #folium.Marker([lat, lon], popup = i.username.decode('utf-8')).add_to(map_1)
            #countttz+=1
        
        map_1.save(r"./map.html")
        self.webView.setHtml(open("./map.html").read())
        self.webView.show()
        
    def drawPositive(self):
        global activeList
        map_2 = folium.Map(location=[average_lat, average_lon])
        activeList = 1
        for i in positiveList:
            lat = i.x
            lon = i.y
            sent = i.mark
            #print(lat)
            #print(lon)
            #print(sent)
            folium.Marker([lat, lon], popup = sent).add_to(map_2)
        
        map_2.save(r"./map.html")
        self.webView.setHtml(open("./map.html").read())
        self.webView.show()
        print(activeList)
            
    def drawNegative(self):
        global activeList
        map_3 = folium.Map(location=[average_lat, average_lon])
        activeList = -1
        for i in negativeList:
            lat = i.x
            lon = i.y
            sent = i.mark
            #print(lat)
            #print(lon)
            #print(sent)
            folium.Marker([lat, lon], popup = sent).add_to(map_3)
        
        map_3.save(r"./map.html")
        self.webView.setHtml(open("./map.html").read())
        self.webView.show()
        print(activeList)
            
    def drawNeutral(self):
        global activeList
        map_4 = folium.Map(location=[average_lat, average_lon])
        activeList = 0
        for i in neutralList:
            lat = i.x
            lon = i.y
            sent = i.mark
            #print(lat)
            #print(lon)
            #print(sent)
            folium.Marker([lat, lon], popup = sent).add_to(map_4)
        
        map_4.save(r"./map.html")
        self.webView.setHtml(open("./map.html").read())
        self.webView.show()
        print(activeList)
        
    def drawNearest(self):
        global activeList
        icon = QtGui.QMessageBox()
        icon.setIcon(QtGui.QMessageBox.Information)
        if activeList == 1:
            theList = point.PointPattern(positiveList)
            text = "Average Nearest Neighbor Distance of Positive Tweets: " + str(theList.nearest_neighbor_KD())
        elif activeList == -1:
            theList = point.PointPattern(negativeList)
            text = "Average Nearest Neighbor Distance of Negative Tweets: " + str(theList.nearest_neighbor_KD())
        elif activeList == 0:
            theList = point.PointPattern(neutralList)
            text = "Average Nearest Neighbor Distance of Neutral Tweets: " + str(theList.nearest_neighbor_KD())
        
        
        icon.setText(text)
        icon.setWindowTitle("Average Nearest Neighbor Distance")
        icon.exec()
            
    def drawG(self):
        global activeList
        gx = [3, 7, 14, 26, 27]
        gy = []
        sum = 0;
        if activeList == 1:
            for i in gx:
                theList = point.PointPattern(positiveList)
                sum = sum+theList.compute_g(i)
                gy.append(sum)
        elif activeList == -1:
            for i in gx:
                theList = point.PointPattern(negativeList)
                sum = sum+theList.compute_g(i)
                gy.append(sum)
        elif activeList == 0:
            for i in gx:
                theList = point.PointPattern(neutralList)
                sum = sum+theList.compute_g(i)
                gy.append(sum)
        
        
        plt.figure(1)
        plt.plot(gx, gy, color='blue', marker='*', linewidth=2)
        plt.show()

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()