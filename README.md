# AI 기반 레시피 추천 서비스 🍽️  

## 개요  
이 프로젝트는 **YOLO v8**을 활용하여 식재료를 인식하고, **Flask** 백엔드를 통해 **React** 프론트엔드로 데이터를 전달한 후, **GPT**를 활용하여 사용자에게 맞춤형 레시피를 추천하는 AI 기반 서비스입니다.  

## 주요 기능  
- **YOLO v8 기반 식재료 인식**: 이미지에서 식재료를 감지 및 분류  
- **Flask API 서버**: YOLO 모델을 통해 식재료를 분석하고 결과를 React로 전송  
- **React 프론트엔드**: 사용자 인터페이스(UI) 제공  
- **GPT 레시피 추천**: 감지된 식재료를 바탕으로 AI가 맞춤형 레시피 추천  

## 기술 스택  
### 모델  
- **YOLO v8**: 식재료 감지 및 분류 ([Ultralytics YOLO](https://github.com/ultralytics/ultralytics))  

### 백엔드  
- **Flask**: API 서버 및 데이터 처리  
- **FastAPI** (선택적 확장 가능)  

### 프론트엔드  
- **React.js**: 사용자 인터페이스(UI) 구현  
- **Tailwind CSS**: UI 스타일링  

### AI 추천  
- **GPT API (OpenAI)**: 감지된 식재료를 기반으로 맞춤형 레시피 생성  
