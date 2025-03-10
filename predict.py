import tensorflow as tf
import numpy as np
from PIL import Image
import json

# 이미지 크기 설정
IMG_HEIGHT = 150
IMG_WIDTH = 150

def load_and_preprocess_image(image_path):
    """이미지를 로드하고 전처리하는 함수"""
    # 이미지 로드
    img = Image.open(image_path)
    # RGB로 변환 (이미지가 RGBA 또는 다른 형식인 경우를 위해)
    img = img.convert('RGB')
    # 크기 조정
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    # 배열로 변환
    img_array = np.array(img)
    # 정규화 (0-1 사이의 값으로)
    img_array = img_array.astype(float) / 255.0
    # 배치 차원 추가
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_garbage(model, image_path, class_names):
    """쓰레기 이미지 분류 예측 함수"""
    # 이미지 전처리
    processed_image = load_and_preprocess_image(image_path)
    
    # 예측
    predictions = model.predict(processed_image)
    predicted_class_index = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_index] * 100
    
    return {
        'class': class_names[predicted_class_index],
        'confidence': confidence
    }

def main():
    # 모델 로드
    try:
        model = tf.keras.models.load_model('garbage_classifier.keras')
        print("모델을 성공적으로 불러왔습니다.")
    except Exception as e:
        print("모델을 불러오는데 실패했습니다:", str(e))
        return

    # 클래스 이름 로드
    try:
        with open('garbage_classes.json', 'r') as f:
            class_names = json.load(f)
        print("클래스 목록:", class_names)
    except Exception as e:
        print("클래스 이름을 불러오는데 실패했습니다:", str(e))
        return

    while True:
        # 사용자로부터 이미지 경로 입력 받기
        image_path = input("\n분류할 이미지 경로를 입력하세요 (종료하려면 'q' 입력): ")
        
        if image_path.lower() == 'q':
            break
            
        try:
            # 예측 수행
            result = predict_garbage(model, image_path, class_names)
            
            # 결과 출력
            print(f"\n예측 결과:")
            print(f"분류: {result['class']}")
            print(f"확신도: {result['confidence']:.2f}%")
            
        except Exception as e:
            print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    main() 