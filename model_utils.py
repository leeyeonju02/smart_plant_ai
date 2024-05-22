import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# 모델 구조를 재정의
def initialize_model():
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),  # 50% 드롭아웃 추가
        nn.Linear(num_ftrs, 3)
    )
    return model

# 이미지를 불러오고 전처리하기 위한 transform 설정
transform = transforms.Compose([
    transforms.Resize((254, 254)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 모델 로드
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = initialize_model()  # 모델 구조 초기화
model.load_state_dict(torch.load('model.pt', map_location=device))  # 학습된 가중치 로드
model.to(device)
model.eval()

def predict_image(image_path):
    # 이미지 불러오기 및 변환
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # 배치 차원 추가

    # 모델로 예측
    with torch.no_grad():
        outputs = model(image.to(device))
        _, preds = torch.max(outputs, 1)

    # 예측된 라벨 반환
    return preds.item()

