from twisted.protocols import basic
from twisted.internet import reactor, protocol
import random
import types 
from imissyou import IMissYou

class MyReceiver(basic.LineReceiver):
	
	delimiter = '\0'
	
	def setGame(self,line):
		if line=="imissyou":
			self.addClass(IMissYou)
		else:
			self.halt("185")

	def addClass(self,newClass):
		self.message = types.MethodType(newClass.message.im_func,self,self.__class__)
		self.error= types.MethodType(newClass.error.im_func,self,self.__class__)

	def connectionMade(self):
		print "Got new client!"
		self.factory.clients.append(self)
		self.state="preinitializing"
		self.id = str(random.randint(0,1000000000))
		print "Connection from" + str(self.transport.getPeer().host)

	def connectionLost(self,reason):
		print "disconnect"
		self.factory.clients.remove(self)
	
	def lineReceived(self,line):
		if line == "<policy-file-request/>":
			print "\t sending policy file"
			self.sendLine("<?xml version=\"1.0\"?><cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"38527\" /></cross-domain-policy>")
		elif self.state=="preinitializing":
			self.setGame(line)
			self.state="initializing"
		else:
			self.message(line)



	def halt(self,msg):
		self.sendLine("ERROR:"+msg)
		self.transport.loseConnection()

class XMLSocket(protocol.Factory):
	
	clients = []

	def __init__(self, protocol=None):
		self.protocol=protocol

def main():
	reactor.listenTCP(38527, XMLSocket(MyReceiver))
	reactor.run()


if __name__ == '__main__':
	main()
