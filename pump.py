from gpiozero import DigitalOutputDevice
import time
import threading
from project_variables import PUMP_PIN

class Pump:
    # check volatile types for access to variable from different threads
    isRunning = False
    
    def __init__(self, pumpPin):
        self.pumpIsActivated = DigitalOutputDevice(pumpPin) 
        
    
    def _activate_pump_for_time_in_s(self, activationTime):
        self.pumpIsActivated.on()
        print("pump on")
        time.sleep(activationTime)
        self.pumpIsActivated.off()
        print("pump off")
        
                
    def pumpVolumeInMl(self, setVolume):
        self.isRunning = True
        calibrationConstant = 30
        activationTime = setVolume/calibrationConstant
        self._activate_pump_for_time_in_s(activationTime)
        self.isRunning = False
        




# this main is for pump testing purposes only
def main():
    pump = Pump(PUMP_PIN)
    pump._activate_pump_for_time_in_s(10.0)


if __name__ == "__main__":
    main()

