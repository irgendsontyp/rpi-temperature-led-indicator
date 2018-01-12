from button_press_handler import ButtonPressHandler
from config import Config
from exit_helper import ExitHelper
from gpio_helper import GPIOHelper
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
import signal
import sys
from temperature_checker import TemperatureChecker, TemperatureCheckerReadError
from temperature_sensor_helper import TemperatureSensorHelper
from temperature_led_switcher import TemperatureLEDSwitcher


exitHelper = ExitHelper()
conf = Config("/etc/temperature-led-indicator/config.conf")

def setupLogger():
	logFormatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
	
	logFileHandler = RotatingFileHandler("/var/log/temperature-led-indicator/status.log", maxBytes = 5 * 1024 * 1024, backupCount = 1, encoding = "utf-8")
	logFileHandler.setFormatter(logFormatter)
	logFileHandler.setLevel(logging.DEBUG)

	logStreamHandler = StreamHandler(sys.stdout)
	logStreamHandler.setFormatter(logFormatter)
	logStreamHandler.setLevel(logging.DEBUG)
	
	logging.getLogger().addHandler(logStreamHandler)
	logging.getLogger().addHandler(logFileHandler)
	
	logging.getLogger().setLevel(logging.DEBUG)


def sigIntHandler(number, stackFrame):
	exitHelper.requestExit()
	
	
def sigTermHandler(number, stackFrame):
	exitHelper.requestExit()


def main():
	setupLogger()
	
	logging.info("*** Application has started, logging has been set up ***")
	
	signal.signal(signal.SIGINT, sigIntHandler)
	signal.signal(signal.SIGINT, sigTermHandler)
	
	logging.info("Handlers for signals SIGINT and SIGTERM have been registered.")

	# Wait for SIGINT or SIGTERM. Button handling is done via a separate thread created by GPIO.add_event_detect	
	with GPIOHelper(conf) as gpioHelper:
		temperatureLedSwitcher = TemperatureLEDSwitcher(gpioHelper)
		temperatureSensorHelper = TemperatureSensorHelper(conf.DeviceIDTemperatureSensor)
		
		temperatureChecker = TemperatureChecker(conf, temperatureLedSwitcher, temperatureSensorHelper, exitHelper)
		
		buttonPressHandler = ButtonPressHandler(temperatureChecker, gpioHelper)
				
		gpioHelper.addButtonPressEventCallback(buttonPressHandler)
			
		logging.info("Button event has been registered. Waiting for button press or exit signals.")
		
		exitHelper.waitForExitRequest()


main()
