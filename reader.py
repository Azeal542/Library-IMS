import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def ScanRFID():
	id, text = reader.read_no_block()
	print(id)
	return id
	GPIO.cleanup() 

#try:
#	id, text= reader.read()
#	print(id)
#	
#finally:
#	GPIO.cleanup()
#
ScanRFID()