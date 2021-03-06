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
import imagezmq

net = cv2.dnn.readNet("data/yolov4_tiny.weights", "data/yolov4_tiny.cfg")     # 객체생성 - 기존의 훈련된 가중치(weight)와 네트워크 구성 저장 파일(cfg) 필요
classes = []
with open("data/coco.names", "r") as f:              
    classes = [line.strip() for line in f.readlines()]          # 클래스 이름을 불러와 저장
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


# vs = cv2.VideoCapture(0)
# vs = cv2.VideoCapture("data/car_on_road.mp4")
# vs = cv2.VideoCapture("http://192.168.0.20:8090/?action=stream")
image_hub = imagezmq.ImageHub()

while True:
    _, frame = image_hub.recv_image()
    image_hub.send_reply(b'OK')


    height, width, channels = frame.shape
    
    imageBlob = cv2.dnn.blobFromImage(frame, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
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

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.01)        # 박스 많은것 제거

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)
        
    # --------------------------------------------------------------------
    # 여기까지 frame에 객체인식된 영상이 저장됨.

    cv2.imshow("Frame", frame)      # 로컬환경에서 출력함.

    key = cv2.waitKey(1) & 0xFF     # 스트리밍영상 'q' 입력시 종료
    if key == ord("q"):
        break

cv2.destroyAllWindows()