import RPi.GPIO as GPIO

class GPIOHelper:
	def __init__(self, conf):
		self.__conf = conf
		
		# Set GPIO numbering mode
		GPIO.setmode(GPIO.BOARD)
		
		# LEDs need output mode
		GPIO.setup(self.__conf.GPIOPinNumberInfoLED, GPIO.OUT, initial = GPIO.LOW)
		GPIO.setup(self.__conf.GPIOPinNumberErrorLED, GPIO.OUT, initial = GPIO.LOW)

		# Button needs input mode
		GPIO.setup(self.__conf.GPIOPinNumberButton, GPIO.IN)
		
		
	def __enter__(self):
		return self
		
		
	def __exit__(self, exc_type, exc_value, traceback):
		GPIO.cleanup()
		
		
	def addButtonPressEventCallback(self, callback):
		GPIO.add_event_detect(self.__conf.GPIOPinNumberButton, GPIO.FALLING, callback = callback) 
		
		
	def switchOnInfoLED(self):
		GPIO.output(self.__conf.GPIOPinNumberInfoLED, GPIO.HIGH)
		
		
	def switchOffInfoLED(self):
		GPIO.output(self.__conf.GPIOPinNumberInfoLED, GPIO.LOW)
		
		
	def switchOnErrorLED(self):
		GPIO.output(self.__conf.GPIOPinNumberErrorLED, GPIO.HIGH)
		
		
	def switchOffErrorLED(self):
		GPIO.output(self.__conf.GPIOPinNumberErrorLED, GPIO.LOW)
