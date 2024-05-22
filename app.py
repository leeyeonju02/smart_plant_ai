from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from model_utils import predict_image

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = '/Users/leeyeonju/Desktop/smart-plant-ai/smart_plant_ai'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/chat/", methods=["POST"])
def chat():
    chatData = request.get_json()
    print(type(chatData))
    print(chatData)
    return jsonify({"open_ai_message": "답변 도착"})

@app.route('/upload/', methods=['POST'])
def upload_file():
    if 'file' not in request.files: 
        return jsonify({"error": "파일의 키가 없습니다"}), 400   
    file = request.files['file'] 
    if file.filename == '': 
        return jsonify({"error": "파일을 선택하지 않았습니다."}), 400
    if file: 
        filename = secure_filename(file.filename) 
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
        file.save(file_path)

        predicted_label = predict_image(file_path)
        return jsonify({"해당 이미지 라벨": predicted_label})
    
    return jsonify({"error": "Something went wrong"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
