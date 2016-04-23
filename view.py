import sys
from PyQt4 import QtGui, QtCore, QtWebKit
import tweet
import folium
import io_geojson
from nose.tools import set_trace

class View(QtGui.QMainWindow):

	def __init__(self):
		self.fetched_tweets = []
		super(View, self).__init__()
		self.initUI()

	def initUI(self):

		map_ = folium.Map(location=[33.4484, -112.0740])
		map_.save(r"./index.html")

		exit = QtGui.QAction(QtGui.QIcon('exit.png'), 'Quit', self)
		exit.setStatusTip('Exit')
		exit.triggered.connect(self.close)
		exit.setShortcut('Ctrl+Q')

		open_ = QtGui.QAction(QtGui.QIcon('open.png'), 'Open File', self)
		open_.setShortcut('Ctrl+F')
		open_.setStatusTip('Import JSON')
		open_.triggered.connect(self.mapTweets)

		positive_tweets = QtGui.QAction(QtGui.QIcon('positive.png'), 'Positive Tweets', self)
		positive_tweets.setStatusTip('Show only positive tweets')
		positive_tweets.triggered.connect(self.positiveTweets)

		negative_tweets = QtGui.QAction(QtGui.QIcon('negative.png'), 'Negative Tweets', self)
		negative_tweets.setStatusTip('Show only negative tweets')
		negative_tweets.triggered.connect(self.negativeTweets)

		neutral_tweets = QtGui.QAction(QtGui.QIcon('neutral.png'), 'Neutral Tweets', self)
		neutral_tweets.setStatusTip('Show only neutral tweets')
		neutral_tweets.triggered.connect(self.neutralTweets)


		self.webView = QtWebKit.QWebView()
		self.webView.setHtml(open(r"./index.html").read())
		self.setCentralWidget(self.webView)

		menubar = self.menuBar()
		menu = menubar.addMenu('&File')
		menu.addAction(exit)
		menu.addAction(open_)

		toolbar = self.addToolBar('Quit')
		toolbar.addAction(exit)
		toolbar = self.addToolBar('Open File')
		toolbar.addAction(open_)
		toolbar = self.addToolBar('Positive Tweets')
		toolbar.addAction(positive_tweets)
		toolbar = self.addToolBar('Neutral Tweets')
		toolbar.addAction(neutral_tweets)
		toolbar = self.addToolBar('Negative Tweets')
		toolbar.addAction(negative_tweets)

		self.setGeometry(300, 400, 700, 500)
		self.setWindowTitle('Map o Tweets')
		self.show()
		self.webView.show()


	def mapTweets(self):
		map_ = folium.Map(location=[33.4484, -112.0740])

		file = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '~')
		if file == '':
			return
		
		tweets = io_geojson.read_tweets(file)
		for t in tweets:
			data = tweet.Tweet(t)
			# folium.Marker([33.4484, -112.0740]).add_to(map_)
			folium.Marker([data.bounds[0][1], data.bounds[0][0]], popup = data.text).add_to(map_)
			self.fetched_tweets.append(data)

		map_.save(r"./index.html")
		self.webView.setHtml(open("./index.html").read())
		self.webView.show()


	def positiveTweets(self):
		map_ = folium.Map(location=[33.4484, -112.0740])
		for t in self.fetched_tweets:
			print(t.sentiment)
			# I'm not sure why the sentiment isn't saving correctly but that's my problem I think
			# still playing around with the Tweet class but it should save sentiment on creation
			# ~ Also probably a smarter way to filter these out than O(n)
			if t.sentiment == 'Positive':
				folium.Marker([t.bounds[0][1], t.bounds[0][0]], popup = t.text).add_to(map_)

	def negativeTweets(self):
		map_ = folium.Map(location=[33.4484, -112.0740])
		for t in self.fetched_tweets:
			print(t.sentiment)
			if t.sentiment == 'Negative':
				folium.Marker([t.bounds[0][1], t.bounds[0][0]], popup = t.text).add_to(map_)

	def neutralTweets(self):
		map_ = folium.Map(location=[33.4484, -112.0740])
		for t in self.fetched_tweets:
			print(t.sentiment)
			if t.sentiment == 'Neutral':
				folium.Marker([t.bounds[0][1], t.bounds[0][0]], popup = t.text).add_to(map_)



def main():
	app = QtGui.QApplication(sys.argv)

	view = View()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()