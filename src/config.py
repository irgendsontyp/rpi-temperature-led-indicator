import configparser


class Config:
	def __init__(self, filename):
		config = configparser.ConfigParser()
		config.read(filename)

		self.__targetTemperature = config["general"].getint("target-temperature")
		self.__maxTemperatureReadTryCount = config["general"].getint("max-temperature-read-try-count")
		self.__temperatureReadSleepInterval = config["general"].getint("temperature-read-sleep-interval")

		# Get GPIO numbers for LEDs and button
		self.__gpioPinNumberInfoLed = config["gpio"].getint("pin_number_info_led")
		self.__gpioPinNumberErrorLed = config["gpio"].getint("pin_number_error_led")
		self.__gpioPinNumberButton = config["gpio"].getint("pin_number_button")

		# Get the device id of the temperature sensor
		self.__deviceIdTemperatureSensorDeviceId = config["sensor"]["device_id"]
		
		
	@property
	def TargetTemperature(self):
		return self.__targetTemperature
		
		
	@property
	def MaxTemperatureReadTryCount(self):
		return self.__maxTemperatureReadTryCount
		
		
	@property
	def TemperatureReadSleepInterval(self):
		return self.__temperatureReadSleepInterval
		
	
	@property
	def GPIOPinNumberInfoLED(self):
		return self.__gpioPinNumberInfoLed
		
		
	@property
	def GPIOPinNumberErrorLED(self):
		return self.__gpioPinNumberErrorLed
		
		
	@property
	def GPIOPinNumberButton(self):
		return self.__gpioPinNumberButton
		
		
	@property
	def DeviceIDTemperatureSensor(self):
		return self.__deviceIdTemperatureSensorDeviceId
