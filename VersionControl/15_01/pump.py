from gpiozero import DigitalOutputDevice
import time

from project_variables import PUMP_PIN

class Pump:
    
    def __init__(self, pumpPin):
        self.pumpIsActivated = DigitalOutputDevice(pumpPin) 
        
    
    def activatePumpForTimeInMs(self, activationTime):
        self.pumpIsActivated.on()
        # therad for time delay
        time.sleep(activationTime)
        self.pumpIsActivated.off()
        
        
    def pumpVolumeInMl(self, volume):
        activationTime = volume/5
        # space for function of volume and time
        self.activatePumpForTimeInMs(activationTime)
        


def main():
    pump = Pump(PUMP_PIN)
    
    pump.pumpVolumeInMl(50)
    
    
    # hugh impedance logic debug
    #pumpOn = DigitalOutputDevice(PUMP_PIN)
    #print("on")
    #pumpOn.on() 
    #time.sleep(10)
    #print("off")
    #pumpOn.off()
    #time.sleep(10)
    



if __name__ == "__main__":
    main()

