import cv2
import imagezmq
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)
 
def gen_frames():  # generate frame by frame from camera

    # 인스턴스 생성
    image_hub = imagezmq.ImageHub()
    
    while True:
        # frame은 openCV image
        # 라즈베리파이에서 전송된 동영상을 이미지 형태로 받음.
        _, frame = image_hub.recv_image()

        # 180도 회전 안 할거면 지우세요.
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # 인코딩한다. 
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 이 코드 필수! 이거 없으면 촬영된 사진!만 나타남.
        image_hub.send_reply(b'OK')

        # 궁극적으로 보여지는 것
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
