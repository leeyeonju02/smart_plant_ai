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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('/path/to/save', filename))
        return "File successfully uploaded"
    return "Something went wrong" 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
