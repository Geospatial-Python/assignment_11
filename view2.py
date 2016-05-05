import os
import sys
from PyQt4 import QtGui, QtWebKit, QtCore
import folium
import tweet
import io_geojson

class View(QtGui.QMainWindow):
		
	def __init__(self):
		super(View, self).__init__()
		self.pos_tweets = []
		self.neg_tweets = []
		self.neu_tweets = []
		self.tweets = []
		self.open()
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
		
		negative = QtGui.QAction('Negative', self)
		negative.triggered.connect(self.display_neg)
		neutral = QtGui.QAction('Neutral', self)
		neutral.triggered.connect(self.display_neu)
		positive = QtGui.QAction('Positive', self)
		positive.triggered.connect(self.display_pos)
		show_all = QtGui.QAction('All', self)
		show_all.triggered.connect(self.display_all)

		calc_g = QtGui.QAction('G Function', self)
		#calc_g.triggered.connect()

		menuBar = self.menuBar()
		sent_menu = menuBar.addMenu('Sentiment')
		sent_menu.addAction(show_all)		
		sent_menu.addAction(positive)
		sent_menu.addAction(neutral)
		sent_menu.addAction(negative)	

		calc_menu = menuBar.addMenu('Calculate')
		calc_menu.addAction(calc_g)	

		toolbar = self.addToolBar('Open')
		toolbar.addAction(load_action)

		self.show()

	def display_neu(self):
		self.plot(self.neu_tweets)

	def display_neg(self):
		self.plot(self.neg_tweets)

	def display_pos(self):
		self.plot(self.pos_tweets)	

	def display_all(self):
		self.plot(self.tweets)

	def open(self):
		file_name = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open Twitter Data', filter='*.json')
		self.tweets_loc = []
		tweet_dic  = io_geojson.read_tweets(file_name)


		for twit in tweet_dic:
			self.tweets.append(tweet.Tweet(twit))
			
		for twet in self.tweets:
			if twet.sentiment == 'Neutral':
				self.neu_tweets.append(twet)
			elif twet.sentiment == 'Negative':
				self.neg_tweets.append(twet)
			else:
				self.pos_tweets.append(twet)
		
		
	def plot(self, tweets):

		for twet in tweets:
			lat = twet.lat[1]
			lng = twet.lng[0]

			folium.Marker([lat, lng], popup=twet.tweet).add_to(self.map)

		self.map.save(self.map_loc)
		self.web_view.load(QtCore.QUrl(self.map_loc))
		print(len(tweets))		

def main():
	app = QtGui.QApplication(sys.argv)
	view = View()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
