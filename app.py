from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = '/Users/leeyeonju/Desktop/smart-plant-ai/smart_plant_ai'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def get(): 
    return ("서버 켜짐")

def predict_image(image_path):
    # 모델 구조를 재정의
    def initialize_model():
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        num_ftrs = model.fc.in_features
        model.fc = nn.Sequential(
        nn.Dropout(0.5),  # 50% 드롭아웃 추가
        nn.Linear(num_ftrs, 3)
        )
        return model
    
    # 모델 로드
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = initialize_model()  # 모델 구조 초기화
    model.load_state_dict(torch.load('model.pt', map_location=device))  # 학습된 가중치 로드
    model.to(device)
    model.eval()

    transform = transforms.Compose([
    transforms.Resize((254, 254)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image = Image.open(image_path).convert('RGB')
    image = transform(image) #이미지 전처리 
    image = image.unsqueeze(0)  # 배치 차원 추가

    # 모델로 예측
    with torch.no_grad():
        outputs = model(image.to(device))
        _, preds = torch.max(outputs, 1)

    # 예측된 라벨 반환
    return preds.item()


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
        return jsonify({"disease_label": predicted_label})
        
    return jsonify({"error": "Something went wrong"}), 500

@app.errorhandler(500)
def handle_500_error(e):
    return jsonify({"error": "서버 점검중입니다."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

