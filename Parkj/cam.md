영상 감시와 객체인식
===
> *참고: https://bong-sik.tistory.com/18?category=775320* , 
> https://ichi.pro/ko/yolov3-mich-opencvleul-sayonghan-gaegche-gamji-28510119961632 , 
> https://deep-eye.tistory.com/15

* 웹캠 실시간 `face detection` 코드와 opencv에 구현된 `yolo` 코드를 함께 참고하였습니다.
* 코드에 쓰인 학습된 yolo 모델 파일 : `yolov4_tiny.weights` , `yolov4_tiny.cfg` , `coco.names` 
* 실습을 위한 영상 파일 : `car_on_road.mp4`

***
# cam.py
```python
from imutils.video import VideoStream
from imutils.video import FPS
from re import T
from numpy.lib.twodim_base import diag
import numpy as np
import imutils
import time
import cv2
import os
import math
import timeit

net = cv2.dnn.readNet("data/yolov4_tiny.weights", "data/yolov4_tiny.cfg")     # 객체생성 - 기존의 훈련된 가중치(weight)와 네트워크 구성 저장 파일(cfg) 필요
classes = []
with open("data/coco.names", "r") as f:              
    classes = [line.strip() for line in f.readlines()]          # 클래스 이름을 불러와 저장
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


#vs = cv2.VideoCapture(0)
vs = cv2.VideoCapture("data/car_on_road.mp4")
time.sleep(2.0)

fps = FPS().start()

while True:
    frame = vs.read()

    # start_t = timeit.default_timer()        # 프레임 시간측정 시작

    # frame = imutils.resize(frame,width=600)
    height, width, channels = frame[1].shape
    
    imageBlob = cv2.dnn.blobFromImage(frame[1], scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(imageBlob)  
    outs = net.forward(output_layers)
    
     # 정보를 화면에 표시
    class_ids = []
    confidences = []
    boxes = []
    vehicle = []    # 추출한 이미지 저장할 배열
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:        # 객체의 신뢰도가 0.1보다 클때 
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                error = 0

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.01)        # 박스 많은것 제거

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i%80]
            cv2.rectangle(frame[1], (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame[1], label, (x, y + 30), font, 3, color, 3)
        
    fps.update()

    # terminate_t = timeit.default_timer()
    # FPS = int(1./(terminate_t - start_t ))      #FRAME 계산

    cv2.imshow("Frame", frame[1])  

    # print(FPS) #FPS 출력

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

fps.stop()
cv2.destroyAllWindows()
# vs.stop()

```

### 1. yolo 구현
```python
net = cv2.dnn.readNet("data/yolov4_tiny.weights", "data/yolov4_tiny.cfg")     # 객체생성 - 기존의 훈련된 가중치(weight)와 네트워크 구성 저장 파일(cfg) 필요
classes = []        # 클래스 수 : (객체의 종류 수)
with open("data/coco.names", "r") as f:              
    classes = [line.strip() for line in f.readlines()]          # 클래스 이름을 불러와 저장
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
```
* 기존에 학습된 yolo 모델을 로드
* 이때 `coco.names`에 입력된 객체의 이름 (ex : car, cup, person ...) 등을 저장

***

### 2. 영상 로드
```python
#vs = cv2.VideoCapture(0)
vs = cv2.VideoCapture("data/car_on_road.mp4")
time.sleep(2.0)

```
* cv2.VideoCapture의 parameter값이 0이면 자동으로 웹캠, 저장된 영상은 상대경로를 기입해주면된다.

***

### 3. 객체 인식후 box 처리
```python
while True:
    frame = vs.read()

    # start_t = timeit.default_timer()        # 프레임 시간측정 시작

    # frame = imutils.resize(frame,width=600)
    height, width, channels = frame[1].shape      # frame[0] = True or False , frame[1] = 실질적인 영상정보가 담긴 클래스로 생각
    
    imageBlob = cv2.dnn.blobFromImage(frame[1], scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(imageBlob)  
    outs = net.forward(output_layers)
    
     # 정보를 화면에 표시
    class_ids = []
    confidences = []
    boxes = []
    vehicle = []    # 추출한 이미지 저장할 배열
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                error = 0
```
* 불러온 영상을 frame에 저장해 프레임 단위로 객체를 인식한다.
* frame의 정보를 저장한다.

