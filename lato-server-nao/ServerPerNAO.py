 from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
 from SocketServer import ThreadingMixIn
 import urllib
 import json
 from urlparse import urlparse,parse_qs
 from naoqi import ALProxy
 import threading
 import logging



class MyClass(GeneratedClass):

	def __init__(self):
		GeneratedClass.__init__(self)
		#
		self.logger.debug("Server start on port 3001")
		#
		self.tts = ALProxy('ALTextToSpeech') # che tipo di proxy e'
		self.tts.post.say("Sono in attesa")
		""" 
			Multithreaded web server in python
			1) definisce il sever su cui rivolger i processi multipli
			2) definisce il tipo di disponibilita' ... server.serve_forever
			3) attiva il xervizio
			4) parte il multi-processo
		"""
		"""
			riga 28, si passono ai costruttori (non visibili) i parametri:
			1) la stringa dell'indirizzo IP/locale e la porta attiva sull IDE di NAO,
			   il dispositivo collegato a NAO
			2) si associa l handler delle richieste/get HTTP, la classe ereditata gestira' 
			   il Listner degli eventi sul web-server
		"""
		self.server = ThreadingServer(("iMac-di-Lucio.local", 51342), NaoHandler)
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.daemon = True
		self.server_thread.start()

def onLoad(self):
	#self.memory = None
	pass

def onUnload(self):
	self.server.shutdown()
	self.server.server_close()
	pass

def onInput_onStart(self):
	#self.onStopped() #activate the output of the box
	#self.recording()
	pass

def onInput_onStop(self):
	self.server.shutdown()
	self.server.server_close()


class NaoHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		"""Responde to a GET request.""" 
		self.protocol_version = 'HTTP/1.1' 
		self.bm = ALProxy("ALBehaviorManager") 
		self.tts = ALProxy('ALTextToSpeech') 
		self.vr = ALProxy('ALVideoRecorder')
		#
		o = urlparse(self.path)
		qs = parse_qs(o.query)
		#
		type = o.path.strip('/')
		#
		if type == 'behavior':
			self.bm.runBehavior(qs['name'][0]) 
		elif type == 'stop' :
			self.bm.stopBehavior(qs['name'][0]) 
		elif type == 'say' :
			self.tts.post.say(qs['text'][0]) 
		elif type == 'stopSay':
			self.tts.post.stopAll() 
		elif type=='motion' :
			str = qs['movement'][0] #motion(qs['movement'][0],float(qs['x'][0]),float(qs['y'][0])) self.mot = ALProxy("ALMotion")
			self.posture = ALProxy("ALRobotPosture")
		#
		if str=='toward' :
			self.posture.goToPosture("StandInit", 0.5)
			self.mot.moveToward(float(qs['x'][0]),float(qs['y'][0]), float( qs['w'][0]), [["Frequency", 0.5]])
		#
		elif str=='rotate' : x =0.2;
			y = 0.2;
			theta = 1.5709; self.mot.moveTo(x, y, theta);
			self.send_response(200) self.send_header('Content-Type', "application/json") self.end_headers()
			self.wfile.write(str)
		return
	
	def motion(movement,x,y):
		mot = ALProxy("ALMotion") 
		if movement=='toward':
			mot.moveToward(x,y, 0.0, [["Frequency", 1.0]]) #if movement=='rotate' :
		#float(qs['x'][0]),float(qs['y'][0])

class ThreadingServer(ThreadingMixIn, HTTPServer): 
	#Multithreaded web server in python
	allow_reuse_address = True
	
	def shutdown(self): 
		self.socket.close() 
		HTTPServer.shutdown(self)
                                                   
