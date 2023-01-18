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
    

def main():
    print("main()")
    flowmeter = Flowmeter(project_variables.FLOWMETER_PIN)
    valve = Valve(project_variables.VALVE_PIN_CLOSE)
    pump = Pump(project_variables.PUMP_PIN)
    
    setupObjectAsInput(flowmeter)
    
    flowmeter.pourLiquidInMl(valve, 2)
    
    print(threading.enumerate())
  
        
 

if __name__ == "__main__":
    main()
