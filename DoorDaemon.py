import threading
import time

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
			elif event.name == "PIN code" and last_card_seen:
				if (event.time - last_card_seen.time) > self.timeout:
					print "timeout failed"
					last_card_seen = None
					continue
				else:
					#check the pin
					#open the door
					if self.card_db.get(last_card_seen.data) == event.data:
						print "open the door!"
					else:
						print "wrong pin!"
					last_card_seen = None




    		self.event_queue.task_done()