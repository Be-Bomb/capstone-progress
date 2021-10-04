Flask 서버와 Pi Camera 연동
===
> *출처: https://neosarchizo.gitbooks.io/raspberrypiforsejonguniv/content/chapter5.html*    


* `세종대 라즈베리파이 교육`의 `파이썬 서버와 파이 카메라 연동` 코드를 가져와 분석해봤습니다. 어떻게 서버가 작동하는지, 어떻게 웹페이지에 동영상 스트리밍 프레임을 띄우는지 등에 대해
 공부해봤습니다.
* 파일은 세 가지로 이루어집니다. templates/index.html, app.py, camera.py
* 여기서 우리는 먼저 `app.py` 코드를 분석하고, `camera.py`의 코드를 분석합니다.

***
# main.py
```python
# app.py
from flask import Flask, render_template, Response
from camera import Camera       # Camera 임포트
"""
camera.py에 있는 Camera 클래스 import
"""


app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

def gen(camera):
   while True:
       frame = camera.get_frame()
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, threaded=True)
```

### 1. import
```python
from camera import Camera
```
* camera.py에 있는 Camera 클래스 


***

### 1. index()
```python
@app.route('/')
def index():
  return render_template('index.html')
```
* 가장 처음에 실행되는 함수다. 
* `render_template`을 통해 templates 폴더 안에 있는 html 파일을 실행시킨다.
* 반드시 templates 폴더 안에 있는 파일만 호출할 수 있다!

***

### 2. gen(camera)
```python
""" Video streaming generator function """
def gen(camera):
   while True:
       frame = camera.get_frame()
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
```
* 파이카메라가 촬영하는 영상을 실시간으로 스트리밍하여 보여주는 function
* `frame = camera.get_frame()`은 비디오 프레임을 가져오는 함수인 것 같다.
* `yield`가 의미하는 바는 잘 모르겠음.

***

### 3. video_feed()
```python
@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()),
                   mimetype='multipart/x-mixed-replace; boundary=frame')
```
* video streaming route. 

***
# camera.py
```python
import time
import io
import threading
import picamera


class Camera(object):
    thread = None
    frame = None
    last_access = 0

    def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                stream.seek(0)
                cls.frame = stream.read()

                stream.seek(0)
                stream.truncate()

                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
```

### 1. import
```python
import time             
import io
import threading
import picamera
```
* `io`: `io`모듈은 스트림 작업을 위한 핵심 도구이다.
* `I/O`에는 세 가지 주요 유형이 있다.
  * text I/O
  * binary I/O
  * raw I/O
* 버퍼링 된 스트림: 버퍼링된 I/O 스트림은 원시 I/O보다 I/O 장치에 대한 더 고수준의 인터페이스를 제공한다.
* `picamera`: 

***
### 2. initialize()
```python
def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)
```
* `threading.Thread(target=self._thread)`: `target`은 `run()` 메소드에의해 호출될 callable 객체이다.
* `threading.start()`: 스레드 활동을 시작한다. 스레드 객체 당 최대 한 번 호출되어야한다. **이 메소드는 같은 스레드 객체에서 두 번 이상 
호출되면 RuntimeError를 발생시킨다.**
* `run()`: 스레드의 활동을 표현하는 메소드. 이 메소드는 target인자로 객체의 생성자에 전달된 callable 객체를 호출한다.

***

### 3. get_frame()
```python
def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame
```

***

### 4. _thread()
```python
 @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)      # 사이즈를 말하는 듯
            camera.hflip = True
            camera.vflip = True

            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                stream.seek(0)
                cls.frame = stream.read()

                stream.seek(0)
                stream.truncate()

                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
```
* `io.BytesIO()`: 이미지를 읽는 방법이다. 이미지를 byte단위로 읽는다. 
* 이미지를 읽는 방법으로는 `cv2.imdecode()`도 있는데, BytesIO보다 연산 속도가 좀 더 빠르다. 동영상 스트리밍에 사용할 수 있을지 확인해봐야겠다.









