FizzPOP-access
==============

FizzPOP DoorGuard

Split into:

	main.py
		Instantiates the various threads and queues and runs them.
	
	Keyboard.py
		Implements a thread that grabs keyboards and packages their outputs into strings then puts these into a queue. This gets the data from the card reader and keypad.

	DoorDaemon.py
		Implements a thread that reads events off the event queue and decides whether or not to open the door

	DoorGuard_db_queries.py
		Talks to the DoorGuard DB
