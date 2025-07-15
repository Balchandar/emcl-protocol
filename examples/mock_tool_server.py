from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/tool/run", methods=["POST"])
def run_tool():
    return jsonify({"status": "tool executed", "echo": request.json})

if __name__ == "__main__":
    app.run(port=5001)
