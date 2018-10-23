import urllib
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):

	nodoBuscado = False
	numeroNodos = 0

	def handle_data(self, data):
		if (self.nodoBuscado):
			print data
			++self.numeroNodos
			if (self.numeroNodos==3):
				self.nodoBuscado = False
		else:
			self.nodoBuscado = (data=="best block")



		

data = urllib.urlopen('http://netstats.testnet.alastria.io.builders/').read()	

parser = MyHTMLParser()
parser.feed(data)