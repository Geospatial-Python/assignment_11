import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import QtCore
import folium
from src import tweet
from src import io_geojson
import random
from multiprocessing import Pool


class LoadingWindow(QtGui.QWidget):
    def __init__(self):
        super(LoadingWindow, self).__init__()
        self.setWindowTitle('Loading, please wait...')
        self.progress_bar = QtGui.QProgressBar(self)
        self.progress_bar.setGeometry(100, 80, 250, 20)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(200, 100, 400, 200)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.show()


class View(QtGui.QMainWindow):

    def __init__(self):
        super(View, self).__init__()

        self.map = None
        self.web_view = None
        self.map_dir = 'tmp/map.html'
        self.init_ui()
        self.popup = None
        self.all_tweets = []

    def init_ui(self):
        # The map will be saved in a temporary directory. Make sure it exists.
        os.makedirs('tmp', exist_ok=True)

        self.web_view = QtWebKit.QWebView()
        self.map = folium.Map(location=[33.4484, -112.0740])
        self.map.zoom_start = 10

        self.map.save(self.map_dir)
        self.web_view.load(QtCore.QUrl(self.map_dir))
        self.setCentralWidget(self.web_view)

        # Define the exit action for use in the toolbar and file menu.
        exit_action = QtGui.QAction(QtGui.QIcon('exit-24.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        # Define the open action.
        open_action = QtGui.QAction(QtGui.QIcon('openFolder.png'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open a Tweet JSON file')
        open_action.triggered.connect(self.open)

        all_action = QtGui.QAction('View All', self)
        all_action.setStatusTip('View all Tweets')
        all_action.triggered.connect(self.display_all)

        positive_action = QtGui.QAction('View Positive', self)
        positive_action.setStatusTip('View positive Tweets')
        positive_action.triggered.connect(self.display_positive)

        negative_action = QtGui.QAction('View Negative', self)
        negative_action.setStatusTip('View negative Tweets')
        negative_action.triggered.connect(self.display_negative)

        neutral_action = QtGui.QAction('View Neutral', self)
        neutral_action.setStatusTip('View neutral Tweets')
        neutral_action.triggered.connect(self.display_neutral)

        # Add a status bar.
        self.statusBar()

        # Add a menu bar, and add a file menu to that.
        menu_bar = self.menuBar()
        # Set the mnemonic to Alt-F.
        # Details: https://msdn.microsoft.com/en-us/library/system.windows.forms.label.usemnemonic(v=vs.110).aspx
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        visualize_menu = menu_bar.addMenu('&Visualization')
        visualize_menu.addAction(all_action)
        visualize_menu.addAction(positive_action)
        visualize_menu.addAction(negative_action)
        visualize_menu.addAction(neutral_action)

        # Add an exit item to the toolbar.
        tool_bar = self.addToolBar('Exit')
        tool_bar.addAction(open_action)
        tool_bar.addAction(exit_action)

        # x, y, width, height
        self.setGeometry(300, 300, 750, 650)
        self.setWindowTitle('Main Window')
        self.show()

        # Put the window in the middle of the screen.
        self.center()

    def center(self):
        geometry = self.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center)
        self.move(geometry.topLeft())

    def open(self):
        file_name = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open Tweet JSON file', filter='*.json')

        # Make sure that the user selected a file to load.
        if not file_name:
            return

        tweets = []
        temp_tweets = io_geojson.read_tweets(file_name)
        for _ in temp_tweets:
            tweets.append(tweet.Tweet(_))
        self.all_tweets = tweets
        self.display_tweets(tweets)

    def display_tweets(self, tweets):
        """

        Parameters
        ----------
        tweets
        A list of Tweet objects.

        Returns
        -------

        """
        self.popup = LoadingWindow()
        average_lat = 0
        average_lon = 0
        handled_tweets = 0

        # Let the garbage collector take care of the old map, instead of manually removing all the old markers.
        self.map = folium.Map(location=[33.4484, -112.0740])
        self.map.zoom_start = 10

        random.seed(1234)

        # Add all tweet locations as markers to the map.
        # Calculate the average lat/lon while iterating.
        for tweet in tweets:
            lat, lon = tweet.gen_point_in_bounds()
            average_lat += lat
            average_lon += lon
            folium.Marker([lat, lon], popup=tweet.tweet).add_to(self.map)
            handled_tweets += 1
            # Show the percent progress in the popup window.
            self.popup.progress_bar.setValue(100 * handled_tweets / len(tweets))

        average_lon /= len(tweets)
        average_lat /= len(tweets)
        self.map.location = [average_lat, average_lon]

        self.map.save(self.map_dir)
        self.web_view.load(QtCore.QUrl(self.map_dir))

        self.popup.close()

    def display_all(self):
        self.display_subset(tweet.Tweet.all)

    def display_positive(self):
        self.display_subset(tweet.Tweet.positive)

    def display_negative(self):
        self.display_subset(tweet.Tweet.negative)

    def display_neutral(self):
        self.display_subset(tweet.Tweet.neutral)

    @staticmethod
    def is_positive(a_tweet):
        return a_tweet.classifier() == tweet.Tweet.positive

    @staticmethod
    def is_negative(a_tweet):
        return a_tweet.classifier() == tweet.Tweet.negative

    @staticmethod
    def is_neutral(a_tweet):
        return a_tweet.classifier() == tweet.Tweet.neutral

    def display_subset(self, selector):
        if len(self.all_tweets) == 0:
            print("No tweets to display.")
            return
        subset = []
        if selector == tweet.Tweet.all:
            subset = self.all_tweets
        else:
            print('Filtering tweets')
            pool = Pool(8)
            f = None
            if selector == tweet.Tweet.positive:
                f = View.is_positive
            elif selector == tweet.Tweet.negative:
                f = View.is_negative
            else:
                f = View.is_neutral
            subset = View.pool_filter(pool, f, self.all_tweets)
            #subset = list(filter(lambda tweet: tweet.classifier() == selector, self.all_tweets))
        print('Displaying tweets')
        self.display_tweets(subset)

    @staticmethod
    def pool_filter(pool, func, candidates):
        """
        A normal functional filter approach may require an excessive amount of runtime
        for large data sets. This function will parallelize that task.
        :param pool: The multiprocessing pool to use to parallelize the task.
        :param func: The filter function (should return True or False if the item should be in the set).
        :param candidates: The set to filter.
        :return: The filtered set.
        """
        # Thanks to:
        # http://ask.sagemath.org/question/7621/howto-implement-filter-for-multiprocessing-module/?answer=11531#post-id-11531
        # for details on implementing this function.
        return [c for c, keep in zip(candidates, pool.map(func, candidates)) if keep]


def main():
    app = QtGui.QApplication(sys.argv)
    view = View()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()