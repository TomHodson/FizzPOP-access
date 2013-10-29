import threading
import time
from RPi import GPIO

#Reads cards swipes and PIN entries from the event_queue,
#opens the door if it spots a correct entry sequence
class DoorDaemon(threading.Thread):
	def __init__(self, event_queue, card_db, timeout = 10):
		self.card_db = card_db
		self.event_queue = event_queue
		self.timeout = timeout
		threading.Thread.__init__(self)
	
	def run(self):
		print "DoorDaemon running"
		last_card_seen = None
		
		while True:
			event = self.event_queue.get(block = True)

			if event.name == "Card Number":
				last_card_seen = event
				print "Card with number {} presented".format(event.data)

			elif event.name == "PIN code" and last_card_seen == None:
					print "Present the card first"

			elif event.name == "PIN code" and (event.time - last_card_seen.time) > self.timeout:
					print "timeout failed, timeout is {} seconds, you took {}".format(
							self.timeout,
							(event.time - last_card_seen.time))
					last_card_seen = None
			elif event.name == "PIN code":
					#check the pin
					#open the door
					if self.card_db.get(last_card_seen.data) == event.data:
						print "open the door!"
						GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
						time.sleep(1)
						GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
						last_card_seen = None
					else:
						print "wrong pin!"




    		self.event_queue.task_done()