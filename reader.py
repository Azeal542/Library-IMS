import atexit
import time

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def ScanRFID(blocking: bool = True, sleep_between_poll: float = 0.1):
	"""Read a tag from the RC522 reader.

	Args:
		blocking: If True, blocks until a tag is present (uses reader.read()).
			If False, polls and returns None if no tag is present.
		sleep_between_poll: Delay between polls when using non-blocking mode.
	"""
	try:
		if blocking:
			id, text = reader.read()
		else:
			id, text = reader.read_no_block()
			if id is None:
				# Avoid a tight busy-loop when no tag is present
				time.sleep(sleep_between_poll)

		if id is not None:
			print(f"RFID scanned: {id}")
		return id
	except Exception as e:
		print("RFID read error:", e)
		time.sleep(0.5)
		return None


def cleanup():
	"""Release GPIO resources used by the RC522 reader."""
	try:
		GPIO.cleanup()
	except Exception:
		pass


# Ensure GPIO is cleaned up when the program exits.
atexit.register(cleanup)

