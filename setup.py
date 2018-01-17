from setuptools import setup, find_packages
import rpitemperatureledindicator

setup(name = "rpi-temperature-led-indicator",
      version = rpitemperatureledindicator.__version__,
      description = "Lights up an LED, then measures the temperature via a DS18B20 sensor connected to a GPIO pin and lights off the LED when a configurable target temperature is reached.",
      author = "irgendsontyp",
      url = "https://github.com/irgendsontyp/rpi-temperature-led-indicator.git",
      dependency_links = ["git+https://github.com/irgendsontyp/python-irgendsontyp-helpers.git/@1.1.0#egg=irgendsontyp-helpers-1.1.0"],
      install_requires = ["irgendsontyp-helpers==1.1.0", "Rpi.GPIO"],
      packages = find_packages()
     )
