from gpiozero import DigitalOutputDevice
import time
import threading


# trzeba wykorzystac watki
class Valve:
    
    def __init__(self, closePin=2):
        self.valveClose = DigitalOutputDevice(closePin)
        self.isThreadActive = 0
        
    def openValve(self, closingTime):
        self.valveClose.off()
        print("valve is being opened")
        time.sleep(closingTime)
        self.valveClose.on()
        print("valve is being closed")
        
    def openForTime(self, openTime):
        openTime = openTime/2
        self.openValve(openTime)
        
    def booleanOpenValve(self, isBeingOpened):
        if ((isBeingOpened == True) and (self.isThreadActive == 0)):
            self.isThreadActive = 1
            defaultOpeningTime = 10.0
            self.valveThread = threading.Thread(target=self.openForTime, args=(defaultOpeningTime,))
            self.valveThread.start()
            print("The thread is alive %s \n", self.valveThread.is_alive())
        elif (isBeingOpened == False):
            self.valveClose.on()                   #czy to jest ladne ze zamykam zawor w innnym miejscu niz w funkcji openValve? (potrzebuje przerwac proces nalewania)

def main():
    valve = Valve()
    valve.openForTime(3.0)
    time.sleep(2.0)
  

if __name__ == "__main__":
    main()
