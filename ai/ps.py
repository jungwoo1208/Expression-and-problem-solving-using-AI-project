from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

# YOLOv8 모델 로드
model = YOLO('C:\\Users\\gjw19\\OneDrive\\바탕 화면\\ai\\test2\\weights\\best.pt')  # 모델 경로를 YOLOv8 모델 파일로 설정

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

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
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'score': score,
                'class_id': class_id
            })

    return jsonify(detections)

if __name__ == '__main__':
    app.run(debug=True)
