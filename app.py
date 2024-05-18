from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

@app.route('/create/', methods=['POST'])
def create(): 
    plantData = request.get_json() 

    print(type(plantData))
    return jsonify({"message": "식물데이터를 성공적으로 받았습니다. "})

@app.route('/chat/', methods=['POST'])
def chat(): 
    chatData = request.get_json()
    print(type(chatData))
    print(chatData)
    return jsonify({"open_ai_message": "답변 도착"})


