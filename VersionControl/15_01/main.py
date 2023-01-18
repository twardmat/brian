import time
import RPi.GPIO as GPIO
from pump import Pump
from valve import Valve
from flowmeter import Flowmeter

import project_variables
# Class Valve includes few sleeps - may interrupt meausrment
# Class pump requires improvment - no sleeps 
def objectInputSetup(instanceSent):
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
    valve = Valve(project_variables.VALVE_PIN_OPEN, project_variables.VALVE_PIN_CLOSE)
    #pump = Pump(project_variables.PUMP_PIN)
    
    objectInputSetup(flowmeter)
    
    try:
        GPIO.add_event_detect(flowmeter.pinNumber, GPIO.RISING)
        lastTime = time.monotonic_ns()
        # valve.openForTime(2.0)
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
        time.sleep(0.01)
 

if __name__ == "__main__":
    main()
