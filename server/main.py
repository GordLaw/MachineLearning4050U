from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/query", methods=["POST"])
def query_model(query_data=None):
    return 0

if __name__ == "__main__":
    print("Starting Flask app...")
    print("Model will load in the background...")
    app.run(host="0.0.0.0", port=8080, debug=False)