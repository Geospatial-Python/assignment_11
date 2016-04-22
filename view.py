import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import QtCore
import folium
from src import tweet
from src import io_geojson
import random


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

    def init_ui(self):
        # This is the central empty widget, to be replaced in a future assignment.
        self.web_view = QtWebKit.QWebView()
        self.map = folium.Map(location=[33.4484, -112.0740])
        self.map.zoom_start = 10

        self.map.save(self.map_dir)
        self.web_view.load(QtCore.QUrl(self.map_dir))
        self.setCentralWidget(self.web_view)

        # The map will be saved in a temporary directory. Make sure it exists.
        os.makedirs('tmp', exist_ok=True)

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

        # Add a status bar.
        self.statusBar()

        # Add a menu bar, and add a file menu to that.
        menu_bar = self.menuBar()
        # Set the mnemonic to Alt-F.
        # Details: https://msdn.microsoft.com/en-us/library/system.windows.forms.label.usemnemonic(v=vs.110).aspx
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

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
            folium.Marker([lat, lon], popup=tweet.username).add_to(self.map)
            handled_tweets += 1
            # Show the percent progress in the popup window.
            self.popup.progress_bar.setValue(100 * handled_tweets / len(tweets))

        average_lon /= len(tweets)
        average_lat /= len(tweets)
        self.map.location = [average_lat, average_lon]

        self.map.save(self.map_dir)
        self.web_view.load(QtCore.QUrl(self.map_dir))

        self.popup.close()


def main():
    app = QtGui.QApplication(sys.argv)
    view = View()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()