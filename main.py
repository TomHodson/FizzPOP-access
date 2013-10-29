from keyboard import KeyBoardReader, cardreader_keymap, keypad_keymap
from DoorDaemon import DoorDaemon
import Queue
from DoorGuard_db_queries import get_card_cache

from evdev import list_devices, InputDevice

devices = {dev.name : dev for dev in map(InputDevice, list_devices())}
print devices
keypad_path = devices["USB Compliant Keypad"].fn
cardreader_path = devices["SONiX USB Device"].fn

event_queue = Queue.Queue()

#card_db = get_card_cache()
card_db = {'0694682760':'5555'}

 #######  Threads   ##### 
#these threads read events form the two USB HID devices and package them up into larger actions
keypad_daemon = KeyBoardReader("PIN code", keypad_path, event_queue, keypad_keymap)
cardreader_daemon = KeyBoardReader("Card Number", '/dev/input/event11', event_queue, cardreader_keymap)
daemon = DoorDaemon(event_queue, card_db, timeout = 10) #reads from the event_queue and opens the door

cardreader_daemon.start()
keypad_daemon.start()
daemon.start()