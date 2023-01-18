#from gpiozero import DigitalOutputDevice
import time
import RPi.GPIO as GPIO
from project_variables import FLOWMETER_PIN
# pin number may be initialised incorrectly

class Flowmeter(object):

    def __new__(cls, FLOWMETER_PIN):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Flowmeter, cls).__new__(cls)
        return cls.instance
    
    def __init__(self, FLOWMETER_PIN):
        self.pinNumber = FLOWMETER_PIN
        self._reset()
        
    def _reset(self):
        self.totalVolume = 0
        self._circleBuffer = [None for i in range(10)]
        self.previousMeasurementTime = None
        self.lastTime = time.monotonic_ns()
     
    def _addToBuffer(self, value):
        self._circleBuffer.pop(0)
        self._circleBuffer.append(value)
        
    def _measurePeriod(self):
        currentTime = time.monotonic_ns()
        if self.previousMeasurementTime != None:
            elapsedTime = currentTime - self.previousMeasurementTime
            self._addToBuffer(elapsedTime)
        
        self.previousMeasurementTime = currentTime
        
    def calculatePeriodMedianInSeconds(self):
        if self._circleBuffer[0] != None:
            sortedBuf = self._circleBuffer.copy()
            sortedBuf.sort()
            midElement = round(len(sortedBuf)/2)
            return sortedBuf[midElement] / 1e9
        return 0
     
    def calculateFrequency(self):
        period = self.calculatePeriodMedianInSeconds()
        if (period != 0):
            return 1 / period
        return None
    
    def calculateTotalVolume(self):
        period = self.calculatePeriodMedianInSeconds()
        if (period != 0):
            secondsInMinute = 60
            flowmeterConstant = 73
            self.totalVolume += secondsInMinute/flowmeterConstant 
        return self.totalVolume
    
    def pourLiquidInMl(self, currentValve, setVolume):
        try:
            GPIO.add_event_detect(self.pinNumber, GPIO.RISING)
            self._reset()
            
            while True:
                if self.totalVolume < setVolume/2:
                    currentValve.booleanOpenValve(True)
                else:
                    currentValve.booleanOpenValve(False)
                
                if GPIO.event_detected(self.pinNumber):
                    self._measurePeriod()
                    
                if((self.lastTime + 1e9) < time.monotonic_ns()):
                    self.lastTime = time.monotonic_ns()
                    self.printObjectVariables()
        finally:
            print("Finally")
            GPIO.remove_event_detect(self.pinNumber)
            if(currentValve.isThreadActive == 1):         # check is_alive() method
                currentValve.valveThread.join()
            
    def printObjectVariables(self):
        print(f"Frequency is equal to {self.calculateFrequency()}")
        print(f"Flow time is {self.calculatePeriodMedianInSeconds()}")
        print(f"Total volume {self.calculateTotalVolume()}")
        
        


# interrupt
# GPIO.add_event_detect(FLOWMETER_PIN, GPIO.RISING, pulseWidthMeasurement)
# callback was adding times to the buffer and every 1 second the median was calculated

def main():
    print("main()")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FLOWMETER_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    flowmeterState = GPIO.input(FLOWMETER_PIN) # interpreter crashes without this line
    try:
        flowmeter = Flowmeter(FLOWMETER_PIN)
        GPIO.add_event_detect(FLOWMETER_PIN, GPIO.RISING)
        lastTime = time.monotonic_ns()
        totalVolume = 0
        while True:
            # time.sleep(1)
            if GPIO.event_detected(FLOWMETER_PIN):
                flowmeter._measurePeriod()
                totalVolume = flowmeter.calculateTotalVolume()
                
            if((lastTime + 1e9) < time.monotonic_ns()):
                lastTime = time.monotonic_ns()
                print(f"Frequency is equal to {flowmeter.calculateFrequency()}")
                print(f"Flow time is {flowmeter.calculatePeriodMedianInSeconds()}")
                print(f"Total volume {totalVolume}")
    finally:
        print("Finally")
        GPIO.remove_event_detect(FLOWMETER_PIN)
        time.sleep(0.01)


if __name__ == "__main__":
    main()

