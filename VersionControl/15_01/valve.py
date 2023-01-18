from gpiozero import DigitalOutputDevice
import time

# trzeba wykorzystac watki
class Valve:
    
    def __init__(self, openPin=2, closePin=4):
        self.valveOpen = DigitalOutputDevice(openPin)
        self.valveClose = DigitalOutputDevice(closePin)
    
    def openValve(self, openingTime):
        self.valveOpen.off()
        self.valveClose.on()
        print("valve is being closed")
        time.sleep(openingTime)
        print("valve is closed")
        self.valveClose.off()
        
    def closeValve(self, closingTime):
        self.valveOpen.on()
        self.valveClose.off()
        print("valve is being opened")
        time.sleep(closingTime)
        print("valve is opened")
        self.valveOpen.off()
        
    def openForTime(self, openTime):
        self.openValve(openTime)
        time.sleep(1.0)
        self.closeValve(openTime)

def main():
    valve = Valve()
    valve.openValve(3.0)
    time.sleep(2.0)
    valve.closeValve(2.0)

if __name__ == "__main__":
    main()
