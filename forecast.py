from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.config["DEBUG"] = False
    app.run(host='localhost', port=5000)
