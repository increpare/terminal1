from twisted.protocols import basic
from twisted.internet import reactor, protocol
import random
import traceback
import datetime

class IMissYou:
	def __init__(self):
		pass

	def message(self,message):
		if self.state=="initializing":
			if message=="principal":
				self.principal=True
				self.sendLine(self.id)
				self.state="alone"
				print "alone"
			else:
				self.principal=False
				self.otherid=message
				#find other connection and link it to this one	
				for c in self.factory.clients:
					if not hasattr(c,'id'):
						continue
					if c.id == self.otherid:
						if hasattr(c,'otherid'):
							print "duplicate client"
							self.halt("duplicate client")
							return
						else:
							c.otherid=self.id 
							c.other=self
							self.other=c
							c.state="togethera"
							self.state="togetherb"
							print "togethera/b"

							print c.transport.getPeer().host
							print self.transport.getPeer().host

							if c.transport.getPeer().host==self.transport.getPeer().host:
								print "local"
								self.sendLine("LOCAL")
								self.other.sendLine("LOCAL")
								#self.error()
							break
				if not hasattr(self,'other'):
					self.error(" - no partner")
				else: 
					print "id pair" + self.id + " , " + self.otherid

		elif self.state=="alone":
			pass
		elif self.state=="togethera":
			pass
		elif self.state=="togetherb":
			if message=="call":
				self.state="calling"
				self.other.state="called"
				self.other.sendLine("ring")
			else:
				self.error("bad message")
		elif self.state=="calling":
			pass
		elif self.state=="called":
			if message=="pickup":
				self.sendLine("connect")
				self.other.sendLine("connect")
		print message
		
	#close connection and sibling connection if there is one		
	def error(self,msg):
		print datetime.date.today()
		print "ERROR:"+msg
		traceback.print_stack();
		for c in self.factory.clients:
			if hasattr(c,"id") and hasattr(c,"otherid") and hasattr(self,"id") and hasattr(self,"otherid"):
				if c.id==self.otherid or c.otherid == self.otherid:
					c.halt(msg)
