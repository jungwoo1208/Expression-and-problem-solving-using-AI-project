from ultralytics import YOLO
import sys
import openai
import os

# OpenAI API 키 설정 (환경 변수 사용 권장)
openai.api_key = ''

def detect_objects(image_path):
    # 학습된 모델 경로를 지정하여 모델 로드
    model = YOLO(r'test2\\weights\\last.pt')

    # 이미지에서 객체 탐지 수행
    results = model(image_path)
    
    detected_classes = set()

    # 탐지된 객체의 클래스 수집
    for result in results:
        for box in result.boxes:
            cls = int(box.cls)  # 클래스
            detected_classes.add(cls)
    
    return detected_classes

def create_class_names_map():
    return {
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
        44: "햄"
    }

def suggest_recipes_via_chatgpt(detected_class_names):
    prompt = f"Detected ingredients: {', '.join(detected_class_names)}. 이 재료로 만들수 있는 요리 레시피를 추천해줘."

    response = openai.Completion.create(
        engine="gpt-4o",  # gpt-4 엔진은 현재 명칭이 다릅니다. gpt-4 엔진으로 변경 필요
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("Error: No image path provided.")
        sys.exit(1)
        
    try:
        detected_classes = detect_objects(image_path)
        
        class_names_map = create_class_names_map()
        detected_class_names = {class_names_map[cls] for cls in detected_classes}
        
        print("Detected objects:", detected_class_names)
        
        if detected_class_names:
            recipes = suggest_recipes_via_chatgpt(detected_class_names)
            print(recipes)
        else:
            print("감지된 재료가 없습니다.")
    except Exception as e:
        print(f"An error occurred: {e}")
