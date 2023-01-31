import time
import threading
import RPi.GPIO as GPIO
from pumpService import PumpService
from valve import Valve
from flowmeter import Flowmeter

import project_variables
# Class Valve includes few sleeps - may interrupt meausrment
# Class pump requires improvment - no sleeps 
def setupObjectAsInput(instanceSent):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(instanceSent.pinNumber, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    flowmeterState = GPIO.input(instanceSent.pinNumber) # interpreter crashes without this line
    
def initialize_liquids():
    flowmeter = Flowmeter(project_variables.FLOWMETER_PIN)
    valve = Valve(project_variables.VALVE_PIN_CLOSE)
    pumpService = PumpService()
    setupObjectAsInput(flowmeter)
    return flowmeter, valve, pumpService
    
    
def main():
    print("main()")
    flowmeter, valve, pumpService = initialize_liquids()
    
    try:
        pumpService.pump_softdrink_in_ml(45)      #this has to be before flowmeter, otherwise there is no concurrency
        flowmeter.pourLiquidInMl(valve, 45)
    
    finally:      
        print(threading.enumerate())


if __name__ == "__main__":
    main()
