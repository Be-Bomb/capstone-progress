## 📁디렉토리 설명
> https://github.com/jeffbass/imagezmq 사용하여 파이 카메라로 촬영된 영상을 PC 서버로 가져옴.
* **`pi-server`**: **라즈베리파이에 다운로드**한다. 파이 카메라로부터 촬영된 영상을 직접 가져와 PC서버로 전송한다.
* **`stream-server`**: **PC에 다운로드**한다. 라즈베리파이로부터 받은 영상을 웹에서 스트리밍하여 볼 수 있도록 한다.    

## 🤷‍♀️실행 방법
각 디렉토리로 이동한 후, 아래를 각각 터미널에 입력한다.

> ### stream-server
```python
# 터미널에 작성
# 둘 중 파이썬 버전에 맞는 것으로 하나 선택해서 사용한다.
python3 server.py
python server.py
```

> ### pi-server
```python
# 터미널에 작성
# 둘 중 파이썬 버전에 맞는 것으로 사용한다.
# 아마 라즈베리파이 안에 설치하는 것은 python3라서 첫 번째 사용하면 될 듯.
python3 cam.py
python cam.py
```

## ⛔발생할 수 있는 오류들
* `imutils` module 관련 에러: 그냥 `pip install imutils` or `pip3 install imutils` 해주기. 이것도 본인 버전에 맞게. 라즈베리파이는 `pip3`로 하기.
* `zmp` module 관련 에러: 이것도 위와 같이 설치
