# !/usr/bin/env python
#@Author: Prem Narain
from twisted.internet import reactor
from starpy import fastagi
import logging
from datetime import datetime
from random import choice
# log = logging.getLogger( 'Greeting')
class Online():
	"""
	5 to 11:59am Good Morning
	12 to 17:59pm 	 Good Noon
	18 to 20:59pm   Good Evening
	21 to 4:59am Good Night
	"""
	def __init__(self):
		self.gret=["Hello","Hi","Hey"]
		self.morning = ["Good morning"]
		self.noon=["Good afternoon","Good Noon"]
		self.evening = ["Good evening"]
		self.night=["Good Night"]
		
	def random(self):
		if datetime.now().hour<12:
			return choice(self.gret) + choice(self.morning) 
		if (datetime.now().hour>12) or (datetime.now().hour< 18):
			return choice(self.gret) + choice(self.noon)
		if (datetime.now().hour>18) or (datetime.now().hour< 21):
			return choice(self.gret) + choice(self.evening)
		if (datetime.now().hour>21) or (datetime.now().hour<5):
			return choice(self.gret) + choice(self.night)

def Greetingflow(agi):
	online=Online()
	log.debug('Greeting of the day')
	Myflow = fastagi.InSequence()
	Myflow.append( agi.answer)
	Myflow.append(agi.sayAlpha,online.random())
	Myflow.append(agi.finish)
	def onFailure( reason ):
		log.error( "Failure: %s", reason.getTraceback())
		agi.finish()
	return Myflow().addErrback( onFailure )
if __name__ == "__main__":
	logging.basicConfig()
	fastagi.log.setLevel(logging.DEBUG )
	f = fastagi.FastAGIFactory(Greetingflow)
	print ("Listening!")
	reactor.listenTCP(4573, f, 50, '127.0.0.1') # only binding on local interface
	reactor.run()
