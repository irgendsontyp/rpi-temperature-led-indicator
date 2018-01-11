import logging
import temperature_sensor_helper
from temperature_sensor_helper import TemperatureCRCError
import time


class TemperatureCheckerReadError(Exception):
	pass


class TemperatureChecker:
	def __init__(self, conf, temperatureEventHandler, temperatureHelper, exitHelper):
		self.__conf = conf
		self.__temperatureEventHandler = temperatureEventHandler
		self.__temperatureHelper = temperatureHelper
		self.__exitHelper = exitHelper
		
		self.__maxTemperatureReadTryCount = conf.MaxTemperatureReadTryCount
	
	
	def start(self):
		self.__temperatureEventHandler.notifyTemperatureReadBegins()
		
		temperatureNotSinking = True
		oldTemperature = None
		currentTemperature = None
		readTriesLeft = self.__maxTemperatureReadTryCount
		
		tryReadTemperature = True
		
		logging.info("Waiting for temperature to sink or to reach target level.")
		
		# Loop while temperature is not sinking
		while (True): 
			# Remember old temperature
			oldTemperature = currentTemperature
			
			
			# Try to read temperature		
			currentTemperature = self.__tryReadTemperature(5)			
			
			if (oldTemperature is not None):
				logging.info("Temperature was read successfully. Old temperature was at " + str(oldTemperature) + "°C, current temperature is at " + str(currentTemperature) + "°C.") 
			
			
			# Check if temperature is sinking or has already reached target level
			if (currentTemperature <= self.__conf.TargetTemperature or (oldTemperature is not None and currentTemperature < oldTemperature)):
				logging.info("Target temperature has been reached or temperature is sinking.")
				break
				
				
			if (not self.__exitHelper.sleepWhileNotExitRequested(self.__conf.TemperatureReadSleepInterval)):
				logging.info("Temperature sink check loop: Quitting, because application exit has been requested.")
				
				return
				
				
		
		logging.info("Waiting for temperature to reach " + str(self.__conf.TargetTemperature) + "°C.")
		
		while (True):		
			temperature = self.__tryReadTemperature(5)

			if (temperature <= self.__conf.TargetTemperature):
				logging.info("Temperature has reached target level of " + str(self.__conf.TargetTemperature) + "°C.")
				
				self.__temperatureEventHandler.notifyTargetTemperatureReached()
				
				break
				
								
			if (not self.__exitHelper.sleepWhileNotExitRequested(5)):
				logging.info("Temperature target level check loop: Quitting, because application exit has been requested.")
				
				return
	
	
	def __tryReadTemperature(self, tryCount):
		readTriesLeft = tryCount
		
		while (readTriesLeft > 0):
			try:
				logging.info("Trying to read temperature. Tries left: " + str(readTriesLeft) + ".")
				
				temperature = currentTemperature = self.__temperatureHelper.readTemperature()
				
				logging.info("Temperature of " + str(temperature) + "°C was successfully read")
				
				return temperature
			except (IOError, TemperatureCRCError) as error:
				readTriesLeft -= 1
				
				logging.error("Error reading temperature: " + str(error) + ".")
				
				
			if (not self.__exitHelper.sleepWhileNotExitRequested(5)):
				logging.info("Exitting temperature read loop because application exit has been requested.")
								
				return
				
		raise TemperatureCheckerReadError()
