import os
import shutil
import random
from tqdm import tqdm

def collect_files(base_dir):
    class_files = {}
    for root, _, filenames in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == ".":
            continue
        class_name = os.path.basename(root)
        if class_name not in class_files:
            class_files[class_name] = []
        for filename in filenames:
            if os.path.isfile(os.path.join(root, filename)):
                class_files[class_name].append(os.path.join(root, filename))
    return class_files

def split_dataset(image_dir, label_dir, train_image_dir, test_image_dir, train_label_dir, test_label_dir, split_ratio=0.8):
    # 폴더가 존재하지 않으면 생성
    os.makedirs(train_image_dir, exist_ok=True)
    os.makedirs(test_image_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(test_label_dir, exist_ok=True)

    # 클래스별로 이미지 파일 목록과 라벨 파일 목록을 가져옵니다
    image_files_by_class = collect_files(image_dir)
    label_files_by_class = collect_files(label_dir)
    
    for cls in image_files_by_class:
        if cls not in label_files_by_class:
            print(f"No matching labels for class {cls}, skipping...")
            continue
        
        image_files = sorted(image_files_by_class[cls])
        label_files = sorted(label_files_by_class[cls])
        
        # 디버깅을 위한 출력
        print(f"Class {cls}: Found {len(image_files)} image files and {len(label_files)} label files.")
        
        # 파일 이름에서 확장자를 제거한 후 매칭
        image_file_basenames = {os.path.splitext(os.path.basename(f))[0]: f for f in image_files}
        label_file_basenames = {os.path.splitext(os.path.basename(f))[0]: f for f in label_files}
        
        matching_keys = image_file_basenames.keys() & label_file_basenames.keys()
        
        image_files = [image_file_basenames[k] for k in matching_keys]
        label_files = [label_file_basenames[k] for k in matching_keys]
        
        # 디버깅을 위한 출력
        print(f"Class {cls}: Matching {len(image_files)} image files and {len(label_files)} label files after filtering.")
        
        # 파일을 8:2 비율로 섞고 분할
        combined = list(zip(image_files, label_files))
        random.shuffle(combined)
        split_index = int(len(combined) * split_ratio)
        train_files = combined[:split_index]
        test_files = combined[split_index:]

        # 파일 이동 - 훈련 데이터
        print(f"Moving training files for class {cls}...")
        for image_file, label_file in tqdm(train_files):
            shutil.move(image_file, os.path.join(train_image_dir, os.path.basename(image_file)))
            shutil.move(label_file, os.path.join(train_label_dir, os.path.basename(label_file)))

        # 파일 이동 - 테스트 데이터
        print(f"Moving testing files for class {cls}...")
        for image_file, label_file in tqdm(test_files):
            shutil.move(image_file, os.path.join(test_image_dir, os.path.basename(image_file)))
            shutil.move(label_file, os.path.join(test_label_dir, os.path.basename(label_file)))

    print("Dataset split complete.")

# 경로 설정
image_dir = r'C:\Users\gjw19\OneDrive\바탕 화면\data\images'
label_dir = r'C:\Users\gjw19\OneDrive\바탕 화면\data\labelyolo'
train_image_dir = r'C:\Users\gjw19\OneDrive\바탕 화면\data\train\images'
test_image_dir = r'C:\Users\gjw19\OneDrive\바탕 화면\data\val\images'
train_label_dir = r'C:\Users\gjw19\OneDrive\바탕 화면\data\train\labels'
test_label_dir = r'C:\Users\gjw19\OneDrive\바탕 화면\data\val\labels'

# 데이터셋 분할
split_dataset(image_dir, label_dir, train_image_dir, test_image_dir, train_label_dir, test_label_dir)
