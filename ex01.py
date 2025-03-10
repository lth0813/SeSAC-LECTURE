import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import json

# 이미지 크기 설정
IMG_HEIGHT = 150
IMG_WIDTH = 150

# 데이터 경로 설정
data_dir = 'data'

# ImageDataGenerator를 사용하여 이미지 로드 및 전처리
datagen = ImageDataGenerator(
    rescale=1./255,  # 픽셀값을 0~1 사이로 정규화
)

# 데이터 로드
dataset = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=32,
    shuffle=True
)

# 클래스 이름 가져오기
class_names = dataset.class_names
print("클래스:", class_names)

# 데이터셋을 리스트로 변환
images = []
labels = []

for image_batch, label_batch in dataset:
    images.extend(image_batch.numpy())
    labels.extend(label_batch.numpy())

images = np.array(images)
labels = np.array(labels)

# train/test 분할 (80:20)
X_train, X_test, y_train, y_test = train_test_split(
    images, labels, 
    test_size=0.2, 
    random_state=42,
    stratify=labels  # 각 클래스의 비율을 유지
)

print("학습 데이터 크기:", X_train.shape)
print("테스트 데이터 크기:", X_test.shape)

# 모델 생성
model = Sequential([
    # 첫 번째 Convolution 층
    # (150, 150, 3) -> (148, 148, 32)
    # 입력 이미지: 150x150 픽셀, 3채널(RGB)
    # 32개의 3x3 필터를 사용하여 특징 추출
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    MaxPooling2D(2, 2),  # (148, 148, 32) -> (74, 74, 32)
    
    # 두 번째 Convolution 층
    # (74, 74, 32) -> (72, 72, 64)
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),  # (72, 72, 64) -> (36, 36, 64)
    
    # 세 번째 Convolution 층
    # (36, 36, 64) -> (34, 34, 64)
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),  # (34, 34, 64) -> (17, 17, 64)
    
    # Flatten 층: 3D -> 1D 변환
    # (17, 17, 64) -> (18496)
    # 2차원 특징 맵을 1차원 벡터로 변환
    Flatten(),
    
    # Dense 층 (완전 연결 층)
    # 18496 -> 64
    Dense(64, activation='relu'),
    
    # Dropout: 과적합 방지
    # 학습 시 64개 뉴런 중 20%를 랜덤하게 비활성화
    Dropout(0.2),
    
    # 출력층
    # 64 -> 6 (쓰레기 분류 카테고리 수)
    # softmax: 각 클래스에 대한 확률 출력
    Dense(len(class_names), activation='softmax')
])

# 모델 컴파일
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 모델 구조 출력
model.summary()

# Early Stopping 설정
early_stopping = EarlyStopping(
    monitor='val_loss',     # 검증 손실을 모니터링
    patience=5,             # 5번의 에포크 동안 개선이 없으면 학습 중단
    restore_best_weights=True,  # 가장 좋은 가중치를 복원
    verbose=1              # 조기 종료 메시지 출력
)

# 학습 설정
EPOCHS = 30  # 최대 에포크 수를 30으로 설정
BATCH_SIZE = 32

# 모델 학습
history = model.fit(
    X_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_data=(X_test, y_test),
    callbacks=[early_stopping],  # Early Stopping 콜백 추가
    verbose=1  # 학습 과정 출력
)

# 학습 결과 시각화
plt.figure(figsize=(12, 4))

# 손실 그래프
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# 정확도 그래프
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()

# 테스트 세트에서 모델 평가
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'\n테스트 정확도: {test_accuracy*100:.2f}%')

# 클래스 이름을 파일로 저장
with open('garbage_classes.json', 'w') as f:
    json.dump(class_names, f)

# 모델 저장
model.save('garbage_classifier.keras')
print("\n모델이 'garbage_classifier.keras'로 저장되었습니다.") 