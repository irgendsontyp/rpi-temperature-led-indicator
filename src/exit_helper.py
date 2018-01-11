import threading
import time


class ExitHelper:
	def __init__(self):
		self.__exitEvent = threading.Event()
		
		
	def isExitRequested(self):
		return self.__exitEvent.is_set()
		
		
	def requestExit(self):
		self.__exitEvent.set()
		
		
	def waitForExitRequest(self):
		self.__exitEvent.wait()
		
		
	def sleepWhileNotExitRequested(self, seconds):		
		for i in range(1, seconds * 100):
			time.sleep(0.01)
			
			if (self.isExitRequested()):
				return False
				
		return True
