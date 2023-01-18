import sys

#sys.path.append('../BRIAN')
from flask import Flask
from main import initialize_liquids
app = Flask(__name__)



@app.route("/")
def hello_world():
    valve.openForTime(10)
    
    return "success"


if __name__ == "__main__":
    valve = initialize_liquids()
    print("Run main")
    app.run(host="0.0.0.0", port=80)
