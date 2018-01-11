class TemperatureLEDSwitcher:
	def __init__(self, gpioHelper):
		self.__gpioHelper = gpioHelper
		
		
	def notifyTemperatureReadBegins(self):
		self.__gpioHelper.switchOnInfoLED()
		
		
	def notifyTargetTemperatureReached(self):
		self.__gpioHelper.switchOffInfoLED()
