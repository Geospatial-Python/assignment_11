import os
import sys
from PyQt4 import QtGui, QtWebKit, QtCore
import folium
import tweet
import io_geojson

class View(QtGui.QMainWindow):
		
	def __init__(self):
		super(View, self).__init__()
		self.init_ui()

	def init_ui(self):
		self.setWindowTitle('Tweets on a Map!')
		self.map_loc = 'map.html'
		self.setWindowIcon(QtGui.QIcon('small.png'))		
		
		self.web_view = QtWebKit.QWebView()
		self.map = folium.Map(location=[33.4255, -111.9400], zoom_start=12)
		self.map.save(self.map_loc)
		self.web_view.load(QtCore.QUrl(self.map_loc))
		self.setCentralWidget(self.web_view)

		load_action = QtGui.QAction(QtGui.QIcon('tweet.png'), 'Exit', self)
		load_action.setShortcut('Ctl+O')
		load_action.triggered.connect(self.open)

		toolbar = self.addToolBar('Open')
		toolbar.addAction(load_action)

		self.show()

	def open(self):
		file_name = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open Twitter Data', filter='*.json')
		self.tweets_loc = []
		tweet_dic  = io_geojson.read_tweets(file_name)
		tweets = []
		for twit in tweet_dic:
			tweets.append(tweet.Tweet(twit))

		for twet in tweets:
			lat = twet.lat[1]
			lng = twet.lng[0]

			folium.Marker([lat, lng], popup=twet.user).add_to(self.map)

		self.map.save(self.map_loc)
		self.web_view.load(QtCore.QUrl(self.map_loc))
		print(len(tweets))		

def main():
	app = QtGui.QApplication(sys.argv)
	view = View()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
