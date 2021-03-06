# !/usr/bin/env python
from twisted.internet import reactor
from starpy import fastagi
import logging,time

log = logging.getLogger( 'answer')
log.setLevel(logging.DEBUG)

class Answer(object):
	'''Answer Class for only answer call'''
	def __init__(self):
		print "Answer Constructor Initialized"
	def __call__(self, agi):
		self.agi = agi
		return self.agi.answer().addCallbacks(self.Answered,self.AnswerFailed)
	def Answered(self,resultline):
		print "Answered Successful"
		self.agi.getData('test',10,1).addCallbacks(self.GetDtmfString,self.FailDtmfString)
		return Hangup()

	def GetDtmfString(self,(dtmfstr,timeoutflag)):
		if timeoutflag:
			print "DTMF Timeout"
		else:
			print "DTMF %s RECEIVED"%[dtmfstr]
	def FailDtmfString(self,reason):
		print "Answer Failed"
	def AnswerFailed(self,reason):
		print "Answer Object Failed"
 
class Hangup(object):
	def __init__(self):
		print "Rejecting Call Object"
   	def __call__(self, agi):
   		self.agi = agi
   		return self.agi.hangup().addCallbacks(self.OnHangupSuccess,self.OnHangupFail)
   	def OnHangupSuccess(self, resultLine):
   		print "Channel Hangup Success"
   		return self.agi.wait(1.0)
   	def OnHangupFail(self,reason):
   		print "Channel Hangup Fail"

class Callflow(object):
	'''Callflow Class for Manage Callflow'''
	def __init__(self):
		print "Callflow Initialized"
	def __call__(self, agi):
		self.agi=agi
		self.current=Answer()
	def __call__(self, agi):
		self.agi= agi
		print "Agi Call Started"
		self.current=Answer()
		return self.current(self.agi).addBoth(self.whatNext)
	def whatNext(self, reason):
		print "Successfully Answered"
	def CallClearing(self,reason):
		print "Call Clearing"
		return self.agi.finish()

if __name__ == '__main__':
	logging.basicConfig()
	fastagi.log.setLevel(logging.DEBUG)
	fun = fastagi.FastAGIFactory(Callflow())
	reactor.listenTCP(4573, fun, 50, '127.0.0.1')
	reactor.run()