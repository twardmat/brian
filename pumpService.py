from pump import Pump
import project_variables
import threading

class PumpService():
    pump  = Pump(project_variables.PUMP_PIN)
    
    def pump_softdrink_in_ml(self, setVolume):
        if self.pump.isRunning:
            print("Pump is running already")
        else:
            print("Pump start")
            self.pumpThread = threading.Thread(target=self.pump.pumpVolumeInMl, args=(setVolume,))
            self.pumpThread.start()
            print(self.pumpThread.is_alive())
        
    def __del__(self):
        self.pumpThread.join()