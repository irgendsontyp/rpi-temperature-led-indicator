import re


class TemperatureCRCError(Exception):
	pass


class TemperatureSensorHelper:
	def __init__(self, deviceId):
		self.__deviceId = deviceId
		
		
	def readTemperatureAsThounsandthPartOfDegrees(self):
		with open("/sys/bus/w1/devices/" + self.__deviceId + "/w1_slave", "r") as f:
			fullString = f.read()

			if (re.search("crc=\w+ YES", fullString)):
				temperatureStringMatch = re.search("t=(\d+)", fullString)
				
				return float(temperatureStringMatch.group(1))
			else:
				raise TemperatureCRCError()
				
				
	def readTemperature(self):
		return self.readTemperatureAsThounsandthPartOfDegrees() / 1000
