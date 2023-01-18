from gpiozero import DigitalOutputDevice
import time
import threading
from project_variables import PUMP_PIN

class Pump:
    
    def __init__(self, pumpPin):
        self.pumpIsActivated = DigitalOutputDevice(pumpPin) 
        
    
    def activatePumpForTimeInMs(self, activationTime):
        self.pumpIsActivated.on()
        time.sleep(activationTime)
        self.pumpIsActivated.off()
        
        
    def pumpVolumeInMl(self, volume):
        activationTime = volume/5
        # space for function of volume and time
        self.activatePumpForTimeInMs(activationTime)
        #self.pumpThread = threading.Thread(target=self.activatePumpForTimeInMs, args=(activationTime,))
        #self.pumpThread.start()







def main():
    pump = Pump(PUMP_PIN)
    pump.pumpIsActivated.off()
    time.sleep(3.0)
    pump.activatePumpForTimeInMs(2000)
    time.sleep(3.0)
    
    
    # high impedance logic debug
    #pumpOn = DigitalOutputDevice(PUMP_PIN)
    #print("on")
    #pumpOn.on() 
    #time.sleep(10)
    #print("off")
    #pumpOn.off()
    #time.sleep(10)
    



if __name__ == "__main__":
    main()

