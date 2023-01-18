from flask import Flask

app = Flask(__name__)



@app.route("/")
def hello_world():
    return "hello motherfuckers"


if __name__ == "__main__":
    print("Run main")
    app.run(host="0.0.0.0", port=80)
