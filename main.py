from keyboard import KeyBoardReader, keymap
from DoorDaemon import DoorDaemon
import Queue
from DoorGuard_db_queries import get_card_cache

event_queue = Queue.Queue()
card_db = get_card_cache()
print card_db

 #######  Threads   ##### 
#these threads read events form the two USB HID devices and package them up into larger actions
keypad_daemon = KeyBoardReader("PIN code", '/dev/input/event10', event_queue, keymap)
cardreader_daemon = KeyBoardReader("Card Number", '/dev/input/event11', event_queue, keymap)
daemon = DoorDaemon(event_queue, card_db, timeout = 10) #reads from the event_queue and opens the door

cardreader_daemon.start()
keypad_daemon.start()
daemon.start()