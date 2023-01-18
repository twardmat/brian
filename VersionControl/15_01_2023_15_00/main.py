import time
import threading
import RPi.GPIO as GPIO
from pump import Pump
from valve import Valve
from flowmeter import Flowmeter

import project_variables
# Class Valve includes few sleeps - may interrupt meausrment
# Class pump requires improvment - no sleeps 
def setupObjectAsInput(instanceSent):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(instanceSent.pinNumber, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    flowmeterState = GPIO.input(instanceSent.pinNumber) # interpreter crashes without this line
    
def printObjectVariables(instanceSent):
    print(f"Frequency is equal to {instanceSent.getFrequency()}")
    print(f"Flow time is {instanceSent.calculatePeriodMedianInSeconds()}")
    print(f"Total volume {instanceSent.calculateTotalVolume()}")




def main():
    print("main()")
    flowmeter = Flowmeter(project_variables.FLOWMETER_PIN)
    valve = Valve(project_variables.VALVE_PIN_CLOSE)
    pump = Pump(project_variables.PUMP_PIN)
    
    setupObjectAsInput(flowmeter)
    
    try:
        GPIO.add_event_detect(flowmeter.pinNumber, GPIO.RISING)
        lastTime = time.monotonic_ns()
        
        
        openTime = 6.0
        valveThread = threading.Thread(target=valve.openForTime, args=(openTime,))
        valveThread.start()
        #valve.openForTime(6.0)
        
        
        
        while True:
            # time.sleep(1)
            if GPIO.event_detected(flowmeter.pinNumber):
                flowmeter.registerMeasurementPeriod()
                                
            if((lastTime + 1e9) < time.monotonic_ns()):
                lastTime = time.monotonic_ns()
                printObjectVariables(flowmeter)
    finally:
        print("Finally")
        GPIO.remove_event_detect(flowmeter.pinNumber)
        #valveThread.join()
        time.sleep(0.01)
        
 

if __name__ == "__main__":
    main()
