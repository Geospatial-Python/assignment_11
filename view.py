from PyQt4 import QtGui, QtWebKit, QtCore
from point_pattern import PointPattern
import os, sys, folium, tweet, io_geojson, random, Plot


class View(QtGui.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        self.map = None
        self.web_view = None
        self.map_dir = 'temp/tweet_map.html'
        self.full_tweet_list = None
        self.tweet_pattern = None
        self.init_ui()
        self.file = None
    def init_ui(self):

        #Make Directory for map
        os.makedirs('temp', exist_ok=True)
        self.web_view = QtWebKit.QWebView()

        #Set location to sky harbor
        self.map = folium.Map(location=[33.4373, -112.0078])

        #zoom out enough to see the entire greater phoenix area
        self.map.zoom_start = 9
        self.map.save('temp/tweet_map.html')
        self.web_view.load(QtCore.QUrl('temp/tweet_map.html'))
        self.setCentralWidget(self.web_view)

        #create a tool bar with the option of opening the Json file
        open_action = QtGui.QAction('Open Json Twitter File', self)
        negative_action = QtGui.QAction('Show Neg Tweets', self)
        pos_action = QtGui.QAction('Show Pos Tweets',self)
        neutral_action = QtGui.QAction('Show Neutral Tweets',self)
        average_nn_action = QtGui.QAction('Compute Average NN Distance',self)
        plot_gfunc_action = QtGui.QAction('Plot G Function',self)


        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_action)

        tweet_menu = menu_bar.addMenu('&Tweet Menu')
        tweet_menu.addAction(negative_action)
        tweet_menu.addAction(pos_action)
        tweet_menu.addAction(neutral_action)

        analytics_menu = menu_bar.addMenu('&Analytics Menu')
        analytics_menu.addAction(average_nn_action)
        analytics_menu.addAction(plot_gfunc_action)

        #the action triggered will cause the open function to execute
        open_action.triggered.connect(self.open)
        negative_action.triggered.connect(self.show_negative_tweets)
        pos_action.triggered.connect(self.show_positive_tweets)
        neutral_action.triggered.connect(self.show_neutral_tweets)
        average_nn_action.triggered.connect(self.disp_average_nn_dist)
        plot_gfunc_action.triggered.connect(self.plot_gfunc)

        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Map of Tweets in Phoenix')
        self.show()

    '''
    Note: I am assuming the user will load a Json file before trying to sort the tweets by negative or not negative
    '''
    def open(self):
        file = QtGui.QFileDialog.getOpenFileName(self, caption='Open Json Twitter File')
        self.file=file
        if not file:
            return

        tweets = []
        tweet_data = io_geojson.read_geojson(file)
        for _ in tweet_data:
            tweets.append(tweet.Tweet(_))
        self.full_tweet_list=tweets
        self.show_folium_marks(tweets)


    def show_negative_tweets(self):
        self.show_folium_marks(self.full_tweet_list,'Negative')
    def show_positive_tweets(self):
        self.show_folium_marks(self.full_tweet_list,'Positive')
    def show_neutral_tweets(self):
        self.show_folium_marks(self.full_tweet_list,'Negative')

    def disp_average_nn_dist(self):
        message = ""

        if self.tweet_pattern is None:
            message = "Select Tweet File First"
            return

        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        text = "Average nearest neighbor distance: "+str(self.tweet_pattern.average_nearest_neighbor_distance_numpy())
        msg.setText(text)
        msg.exec_()

    def plot_gfunc(self):
        data5=self.tweet_pattern.g_func(5)
        data10=self.tweet_pattern.g_func(10)
        data20=self.tweet_pattern.g_func(20)
        data30 = self.tweet_pattern.g_func(30)
        data100 = self.tweet_pattern.g_func(100)

        plot = Plot.Window()

        plot.plot(data5[1],data5[0],'G(5)','red')
        plot.plot(data10[1], data10[0], 'G(10)','blue')
        plot.plot(data20[1], data20[0], 'G(20)','green')
        plot.plot(data30[1], data30[0], 'G(30)','yellow')
        plot.plot(data100[1], data100[0], 'G(100)','pink')

        plot.exec_()

    def show_folium_marks(self, tweets,mark=None):
        self.map = folium.Map(location=[33.4373, -112.0078])
        self.map.zoom_start = 9

        tweet_lat=0
        tweet_lon=0

        #set a maximum number of tweets to process
        limiter=10000
        divisor = 0
        #limiter=len(tweets)
        tweet_pattern = PointPattern()
        #loop through all the tweets
        self.tweet_pattern = None
        for i, tweet in enumerate(tweets):

            if i>limiter-1:
                break

            tweet_point = tweet.gen_rand_pt()
            subpoint=[tweet_point.getx(), tweet_point.gety()]
            if mark=='Negative' and tweet_point.get_mark()=='Negative':
                tweet_lat+=tweet_point.getx()
                tweet_lon+=tweet_point.gety()
                folium.Marker(subpoint,tweet.text).add_to(self.map)
                divisor+=1
                tweet_pattern.add_pt(subpoint)
            elif mark=='Positive' and tweet_point.get_mark()=='Positive':
                tweet_lat+=tweet_point.getx()
                tweet_lon+=tweet_point.gety()
                folium.Marker(subpoint,tweet.text).add_to(self.map)
                divisor += 1
                tweet_pattern.add_pt(subpoint)
            elif mark=='Neutral' and tweet_point.get_mark()=='Neutral':
                tweet_lat+=tweet_point.getx()
                tweet_lon+=tweet_point.gety()
                folium.Marker(subpoint,tweet.text).add_to(self.map)
                divisor += 1
                tweet_pattern.add_pt(subpoint)
            elif mark==None:
                #print('Nonemark')
                tweet_lat+=tweet_point.getx()
                tweet_lon+=tweet_point.gety()
                folium.Marker(subpoint,tweet.text).add_to(self.map)
                divisor += 1
                tweet_pattern.add_pt(subpoint)
        self.tweet_pattern=tweet_pattern
        print('folium printed')
        #make sure to recenter the map to the average of the tweet coordinates
        self.map.location=[tweet_lat/divisor,tweet_lon/divisor]
        #self.map = folium.Map([tweet_lat/len(tweets),tweet_lon/len(tweets)])
        self.map.save('temp/tweet_map.html')
        self.web_view.load(QtCore.QUrl('temp/tweet_map.html'))
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Map of Tweets in Phoenix')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    view=View()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
