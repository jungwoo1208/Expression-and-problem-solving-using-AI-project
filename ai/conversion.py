import os
import json

def convert_to_yolo_format(json_data, class_id):
    yolo_data = []
    for item in json_data:
        point = item.get("Point(x,y)", "")
        if point:
            try:
                center_x, center_y = map(float, point.split(','))
                width = float(item["W"])
                height = float(item["H"])

                yolo_format = f"{class_id} {center_x} {center_y} {width} {height}"
                yolo_data.append(yolo_format)
            except ValueError as e:
                print(f"Error converting point or size for item: {item}, error: {e}")
                continue
        else:
            print(f"Skipping item with empty or invalid 'Point(x,y)': {item}")
    
    return yolo_data

def process_folders(base_folder, output_folder):
    class_mapping = {}
    class_id = 0

    for class_folder in sorted(os.listdir(base_folder)):
        if class_folder.endswith("json"):
            class_name = class_folder.replace("json", "").strip()
            class_folder_path = os.path.join(base_folder, class_folder)
            if os.path.isdir(class_folder_path):
                print(f"Processing folder: {class_folder_path}")
                class_mapping[class_id] = class_name
                class_output_folder = os.path.join(output_folder, class_name)
                os.makedirs(class_output_folder, exist_ok=True)
                
                for json_file in os.listdir(class_folder_path):
                    if json_file.endswith('.json'):
                        json_file_path = os.path.join(class_folder_path, json_file)
                        print(f"Processing JSON file: {json_file_path}")
                        with open(json_file_path, 'r', encoding='utf-8') as file:
                            json_data = json.load(file)
                        
                        if not json_data:
                            print(f"Skipping empty JSON file: {json_file_path}")
                            continue

                        if "Code Name" not in json_data[0]:
                            print(f"Skipping JSON file with missing 'Code Name': {json_file_path}")
                            continue

                        image_name = os.path.splitext(json_data[0]["Code Name"])[0]
                        yolo_data = convert_to_yolo_format(json_data, class_id)

                        if yolo_data:
                            yolo_file_path = os.path.join(class_output_folder, f"{image_name}.txt")
                            with open(yolo_file_path, 'w', encoding='utf-8') as yolo_file:
                                yolo_file.write("\n".join(yolo_data))
                            print(f"Saved YOLO file: {yolo_file_path}")
                        else:
                            print(f"No valid data to write for image: {image_name}")
            
                class_id += 1

    return class_mapping

# 베이스 폴더 경로와 출력 폴더 경로를 지정하세요
base_folder = 'C:/Users/gjw19/OneDrive/바탕 화면/data/label'
output_folder = 'C:/Users/gjw19/OneDrive/바탕 화면/data/labelyolo'

class_mapping = process_folders(base_folder, output_folder)

# 클래스 번호와 폴더명 출력
print("Processing complete. Class ID and Folder Name mapping:")
for class_id, class_folder in class_mapping.items():
    print(f"Class ID: {class_id}, Folder Name: {class_folder}")
