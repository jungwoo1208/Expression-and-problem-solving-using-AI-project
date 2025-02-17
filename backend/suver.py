from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 도메인에 대해 CORS 허용

# YOLOv8 모델 로드
model = YOLO('backend\\best.pt')  # 모델 경로를 YOLOv8 모델 파일로 설정

# 클래스 ID와 재료 이름 매핑
class_id_to_ingredient = {
    0: "가지",
    1: "개맛살",
    2: "고구마",
    3: "고등어",
    4: "김",
    5: "노란파프리카",
    6: "피망",
    7: "달걀",
    8: "닭가슴살",
    9: "당근",
    10: "대파",
    11: "두부",
    12: "마늘",
    13: "쌀",
    14: "배추",
    15: "김치",
    16: "버섯",
    17: "베이컨",
    18: "브로콜리",
    19: "비엔나소시지",
    20: "삼겹살",
    21: "새우",
    22: "소시지",
    23: "숙주나물",
    24: "순대",
    25: "슬라이스치즈",
    26: "시금치",
    27: "쌀",
    28: "밥",
    29: "애호박",
    30: "양배추",
    31: "양파",
    32: "오이",
    33: "오징어",
    34: "적양배추",
    35: "참치캔",
    36: "체다치즈",
    37: "치즈",
    38: "콩나물",
    39: "토마토",
    40: "파프리카",
    41: "노란파프리카",
    42: "빨간파프리카",
    43: "팽이버섯",
    44: "돼지 고기"
}

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        print("No file part in the request.")
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        print("No selected file.")
        return jsonify({'error': 'No selected file'})

    print(f"File received: {file.filename}")

    # 이미지 읽기
    img_bytes = file.read()
    np_img = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # 객체 감지
    results = model(img)
    detections = []
    for result in results:
        for obj in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = obj
            ingredient = class_id_to_ingredient.get(int(class_id), "Unknown")
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'score': score,
                'class_id': class_id,
                'ingredient': ingredient
            })

    print(f"Detections: {detections}")
    return jsonify({'detections': detections})

if __name__ == '__main__':
    app.run(debug=True)
