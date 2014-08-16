#!/usr/bin/env python2.7
import RPi.GPIO as GPIO
import os
import pyinotify
import atexit
import datetime
import string,cgi,time,urlparse, threading, urllib2
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cStringIO import StringIO

#Class Definitions
#Watches the sensor directory for a file named 1 or 0, and toggles the relay based on that
class PTmp(pyinotify.ProcessEvent):
	def process_IN_CREATE(self, event):
		wState = writeState
		cExit = cleanExit
		if event.name == "1":
			global toggle
			wState("on")
			toggle = True
			writeLog("Web toggled on")
			GPIO.output(RELAY,1)
		if event.name == "0":
			writeLog("Web toggled off")
			wState("off")
			toggle = False
			GPIO.output(RELAY,0)
		if event.name == "stop":
			writeLog("Stop request found")
			wState("stopped")
			os.remove("/var/www/sensor/stop")
			cExit()
			exit(0)
		f = open(statepath)
		print f.read() 

stopHTTP = 0
#Handle web requests
class WebHandler(BaseHTTPRequestHandler):
	def response(self,text):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(text)

	def process_state(self,state):
		wState = writeState
		cExit = cleanExit
		if state == "1":
			global toggle
			wState("on")
			toggle = True
			writeLog("Web API toggled on")
			GPIO.output(RELAY,1)
			self.response("On")
		if state == "0":
			writeLog("Web API toggled off")
			wState("off")
			toggle = False
			GPIO.output(RELAY,0)
			self.response("Off")
		if state == "get":
			self.response(str(toggle))

	def do_GET(self):
		try:
			global toggle
			path = self.path
			if '?' in path:
				path, tmp = path.split('?', 1)
				qs = urlparse.parse_qs(tmp)
				print "State:"
				try:
					
					print "State:"
					apistate = qs['state'][0]
					print apistate
					self.process_state(apistate)
				except Exception as e:
					print e
				return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
		except Exception as e:
			#print(e)
			raise

#Thread setup class
class httpThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):
		print "Starting " + self.name
		api_listen_async(self.name, self.counter, 5)
		print "Exiting " + self.name

#endclassdef


#Method Definitions
#log method
def writeLog(data):
	i = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
	l = open(logpath,'a')
	l.write(i + ":" + data + "\n")
	l.close()
#Writes the current state to a file so it can be viewed from other methods
def writeState(state):
		f = open(statepath,'w')
		f.write(state)
		f.close()

#Clean exit of the program, stop notifier and clean up GPIO
def cleanExit():
	print "Quitting"
	global stopHTTP
	stopHTTP = 1
	try:
		content = urllib2.urlopen('http://127.0.0.1:8080').read()
	except:
		pass		
	writeLog("Keyboard Interrupt")
	writeLog("Clean exit called")
	GPIO.cleanup()
	notifier.stop()
	if (os.path.isfile("/var/www/sensor/stop")):
		os.remove("/var/www/sensor/stop")
	writeState("stopped")

#Watch to see if we are shutting down
def keepRunning():
	if (stopHTTP == 0):
		return True
	else:
		return False

#async listen
def api_listen_async(threadName, delay, counter):
	#print "%s: %s" % (threadName, time.ctime(time.time()))
	try:
		print 'started httpserver...'
		server = HTTPServer(('', 8080), WebHandler)
		while keepRunning():
			server.handle_request()
	except KeyboardInterrupt:
		#print '^C received, shutting down server'
		server.socket.close()
	except Exception as e:
		print(e)
		raise

def my_callback(val):
	global toggle
	toggle = not toggle
	GPIO.output(RELAY,toggle)
	if toggle:
		writeState("on")
	else:
		writeState("off")
	writeLog("IR State set to " + str(toggle))
	f = open(statepath)
	print f.read()
#end method def

#Setup and config
IR_SENSOR = 23
RELAY = 24

#Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# GPIO IR_SENSOR set up as input. It is pulled down to stop false signals from a bouncing IR signal
GPIO.setup(IR_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RELAY, GPIO.OUT)

#Setup some variables needed for file watching and our toggle
print "Running..."
toggle = False
wpath = "/var/www/sensor"
statepath = "/var/www/sensor/state"

#Create the pyinotify variables, only watch for creates
wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE
logpath = "/var/log/sensord.log"
	
#Remove the stop file incase it didn't get cleaned up properly (incorrect shutdown perhaps)
if (os.path.isfile("/var/www/sensor/stop")):
	writeLog("Stop file removed")
	os.remove("/var/www/sensor/stop")

#Registers the cleanExit method as the last thing to run when being terminated. This allows the stop command from stop-start-daemon to cleanly
#shut down the sensorw service
atexit.register(cleanExit)

#Adds a watcher to pyinotify
notifier = pyinotify.Notifier(wm, PTmp())
wdd = wm.add_watch(wpath, mask, rec=True)

#Add a gpio event on the IR sensor, when it is a falling signal, it will run my_callback. 
#bouncetime will reduce flapping of the sensor
GPIO.add_event_detect(IR_SENSOR, GPIO.FALLING, callback=my_callback, bouncetime=600)
writeState("ready")
writeLog("Listening for events")
#Main loop to watch for file events. The IR sensor is handled by the callback delegate
thread1 = httpThread(1, "Thread-1", 1)
thread1.start()
#end main setup	


#Start main loop
while True:
	try:
		notifier.process_events()
		if notifier.check_events():
			notifier.read_events()

	except KeyboardInterrupt:
		print "Quitting"
		stopHTTP = 1
		try:
			content = urllib2.urlopen('http://127.0.0.1:8080').read()
		except:
			pass		
		writeLog("Keyboard Interrupt")
		exit(0)
		break
#end main loop
