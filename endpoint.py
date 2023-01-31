import sys

#sys.path.append('../BRIAN')
from flask import Flask
from main import initialize_liquids
from pumpService import PumpService
app = Flask(__name__)



@app.route("/")
def pump_softdrink():
    pump_service.pump_softdrink_in_ml(45)
    print ("%f", 45)
    
    return "Volume was passed to pump"


if __name__ == "__main__":
    #valve = initialize_liquids()
    pump_service = PumpService()
    print("Run main")
    app.run(host="0.0.0.0", port=80)
