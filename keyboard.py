import threading
from evdev import InputDevice, categorize, ecodes
import time
import Queue
from collections import namedtuple

class GrabbedInputDevice(InputDevice):
	def __enter__(self):
		self.grab()
		return self
	def __exit__(self, type, value, traceback):
		self.ungrab()

Event = namedtuple('Event', 'name data time')



class KeyBoardReader(threading.Thread):
    def __init__(self, name, device_path, queue, keymap):
    	"""
		Reads from the given device until a newline character
		then puts it into the queue as a tuple of (name, data, timestamp)
		No timeout implemented, there should be one.
		"""
     	self.dev_name = name
        self.device_path = device_path
        self.buffer = []
        self.queue = queue
        self.keymap = keymap
        threading.Thread.__init__(self)


    def run(self):
    	print self.dev_name + " running\n"
    	
    	with GrabbedInputDevice(self.device_path) as self.device:
	    	for event in self.device.read_loop():
	    		if event.type == ecodes.EV_KEY and event.value == 0: #check it's a key press and that it's a keydown
		    		key = self.keymap.get(event.code)
		    		#store characters that exist in the keymap, puts it on the queue when it hits a '\n'
		    		if key == '\n':
		    			if self.buffer: 
			    			packet = Event(self.dev_name, "".join(self.buffer), event.timestamp())
			    			self.queue.put(packet)
			    			self.buffer = []
			    		continue
			    	if key == 'backspace':
			    		self.buffer.pop()
		        	elif key != None:
		        		self.buffer.append(key)
cardreader_keymap = {
	2:'1',
	3:'2',
	4:'3',
	5:'4',
	6:'5',
	7:'6',
	8:'7',
	9:'8',
	10:'9',
	11:'0',
	28:'\n',
	}


keypad_keymap = {
	79:'1',
	80:'2',
	81:'3',
	75:'4',
	76:'5',
	77:'6',
	71:'7',
	72:'8',
	73:'9',
	82:'0',
	28:'\n',
	83:'.',
	74:'-',
	78:'+',
	98:'/',
	55:'*',
	14:'backspace',
	15:'\t'
	}