from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/chat/", methods=["POST"])
def chat():
    chatData = request.get_json()
    print(type(chatData))
    print(chatData)

    doSomeThing(chatData)

    return jsonify({"open_ai_message": "답변 도착"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
