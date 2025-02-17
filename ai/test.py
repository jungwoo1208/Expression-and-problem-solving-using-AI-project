import cv2
import random
from ultralytics import YOLO

# YOLOv8 모델 로드 (pretrained 모델 사용)
model = YOLO('C:\\jungwoo1208\\ai 활용\\ai\\test2\\weights\\best.pt')  # 'yolov8n.pt' 파일 경로를 학습된 모델로 변경

# 클래스 ID에 대응하는 한국어 라벨 맵
label_map = {
    0: "가지", 1: "개맛살", 2: "고구마", 3: "고등어", 4: "김", 5: "노란파프리카", 6: "피망",
    7: "달걀", 8: "닭가슴살", 9: "당근", 10: "대파", 11: "두부", 12: "마늘", 13: "쌀",
    14: "배추", 15: "김치", 16: "버섯", 17: "베이컨", 18: "브로콜리", 19: "비엔나소시지",
    20: "삼겹살", 21: "새우", 22: "소시지", 23: "숙주나물", 24: "순대", 25: "슬라이스치즈",
    26: "시금치", 27: "쌀", 28: "밥", 29: "애호박", 30: "양배추", 31: "양파", 32: "오이",
    33: "오징어", 34: "적양배추", 35: "참치캔", 36: "체다치즈", 37: "치즈", 38: "콩나물",
    39: "토마토", 40: "파프리카", 41: "노란파프리카", 42: "빨간파프리카", 43: "팽이버섯", 44: "햄"
}

# 이미지 읽기
image_path = 'C:\\Users\\gjw19\\Downloads\가지.jpeg'
image = cv2.imread(image_path)

# 객체 인식 수행
results = model(image)

# 각 객체 주위에 다른 색상으로 박스 그리기
for result in results:
    boxes = result.boxes.xyxy.numpy()  # 객체 박스 좌표 (xmin, ymin, xmax, ymax)
    confidences = result.boxes.conf.numpy()  # 객체 신뢰도
    class_ids = result.boxes.cls.numpy()  # 객체 클래스 ID

    for box, conf, class_id in zip(boxes, confidences, class_ids):
        # 랜덤 색상 생성
        color = [int(c) for c in random.choices(range(256), k=3)]

        # 박스 좌표
        xmin, ymin, xmax, ymax = map(int, box)

        # 박스 그리기
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
        
        # 클래스 이름과 신뢰도 표시
        label = f'{label_map.get(int(class_id), "Unknown")}: {conf:.2f}'
        cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# 결과 이미지 저장 및 표시
cv2.imwrite('annotated_image.jpg', image)
cv2.imshow('YOLOv8 Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
