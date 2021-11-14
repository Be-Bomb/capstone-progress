객체 인식 + 스트리밍 내용 정리
===
# 설명
> * 기존에 imagezmq.py를 이용한 스트리밍 방법 사용([streaming](https://github.com/Be-Bomb/capstone-progress/tree/main/hjkook/docs/streaming/pi-server)) 객체인식코드와 병합.
> * 추후 객체인식코드의 부분을 클래스화 하여 간소화할 예정.
> * 신뢰도 출력에 대해 더 찾아보고 나타날 수 있도록 수정 예정.

# data
> * yolo 모델의 3가지 요소 (cfg, weight, names) 파일 저장

# pi-server
> * pi에서 영상을 넘겨주기 위한 코드, [pi-server](https://github.com/Be-Bomb/capstone-progress/tree/main/hjkook/docs/streaming/pi-server) 와 동일

# detect_streaming.py
> * pi에서 영상을 넘겨받아 객체 인식 진행
> * 영상확인은 local에서 확인이 이루어짐.

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
    
> * flask 스트리밍을 할시 이 frame을 다시 인코딩 후 flask 서버로 옮겨주면 된다.
```python
        # 인코딩한다. 
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 이 코드 필수! 이거 없으면 촬영된 사진!만 나타남.
        image_hub.send_reply(b'OK')

        # 궁극적으로 보여지는 것
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
```
