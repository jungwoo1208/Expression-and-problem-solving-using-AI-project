from ultralytics import YOLO
import cv2

# 학습된 모델 경로를 지정하여 모델 로드
model = YOLO('C:/Users/gjw19/OneDrive/바탕 화면/ai/test1/train_experiment11/weights/best.pt')

# 이미지 파일 경로 지정
image_path = 'C:\\Users\\gjw19\\Downloads\\당감.jpg'

# 이미지에서 객체 탐지 수행
results = model(image_path)

# 결과 시각화 및 출력
for result in results:
    # 결과 시각화
    image_with_boxes = result.plot()  # 결과를 포함한 이미지를 얻습니다.

    # 탐지된 객체의 클래스, 위치, 신뢰도 출력
    for box in result.boxes:
        cls = int(box.cls)  # 클래스
        conf = float(box.conf)  # 신뢰도
        xyxy = box.xyxy.tolist()  # 바운딩 박스 좌표
        print(f"Class: {cls}, Confidence: {conf:.2f}, Bounding Box: {xyxy}")

    # 이미지를 OpenCV 창에서 표시
    cv2.imshow('Detected Objects', image_with_boxes)
    cv2.waitKey(0)  # 키 입력 대기
    cv2.destroyAllWindows()  # 창 닫기
