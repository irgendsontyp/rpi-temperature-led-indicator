import logging
from .temperature_checker import TemperatureCheckerReadError
from threading import Lock

class ButtonPressHandler:
	def __init__(self, temperatureChecker, gpioHelper):
		self.__temperatureChecker = temperatureChecker
		self.__gpioHelper = gpioHelper
		self.__lock = Lock()
	
	
	def __call__(self, pin):		
		if (self.__lock.acquire(blocking = False)):
			try:
				logging.info("Starting temperature read procedure.")
			
				self.__gpioHelper.switchOffErrorLED()
			
				self.__temperatureChecker.start()
			except Exception as error:
				logging.error("An error occured: " + str(error) + ". Switching on error LED.")
				
				self.__gpioHelper.switchOnErrorLED()
			finally:
				self.__lock.release()
		else:
			logging.info("Lock could not be aquired.")
