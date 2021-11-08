# [`이경로`](https://github.com/thispath98)의 캡스톤 디자인을 위한 공부 자료입니다.

## 담당 파트
1. YOLO
2. Raspberry Pi ↔️ Flask Server
---

## ✍️  Issues
> opencv와 Flask를 통해 통신하는 것은 많은 예제 코드가 있어서 문제가 되지 않는다. 핵심은 `잘 학습된 모델`과 `촬영한 영상을 서버로 옮기는 것`.

> 서버에서 스트리밍 영상을 객체 탐지를 한다. 라즈베리 파이를 서버로 할지와 외부 서버를 이용할지가 고민인데, 라즈베리 파이 연산 속도가 이를 감당할 수 없을 것 같아 `외부 서버`를 이용할 것 같다.

## ✍️ 참고할 자료

1. 라즈베리 파이
    * [파이 카메라, 웹으로 전송](https://upcake.tistory.com/355)
    * [세종대 라즈베리 파이 교육](https://neosarchizo.gitbooks.io/raspberrypiforsejonguniv/content/chapter5.html)
    * [라즈베리파이 카메라 모듈 사용](http://www.3demp.com/community/boardDetails.php?cbID=233)
    * [라즈베리파이로 CCTV 만들기](https://github.com/kairess/cctv_raspberrypi) | [유튜브](https://youtu.be/DIGwweDJCBk) | [티스토리](https://wonpaper.tistory.com/383) / 라즈베리파이 카메라를 서버로 tcp를 이용해서 전송한다.

2. 웹 스트리밍
    * [mjpg-streamer를 사용한 웹 스트리밍을 OpenCV에서 가져오기](https://webnautes.tistory.com/1262) | [깃허브](https://github.com/jacksonliam/mjpg-streamer) (우리의 라즈베리 파이는 opencv 3인 것 같다.)
    * [OpenCV 및 Flask를 사용하여 웹 브라우저에서 비디오 스트리밍](https://ichi.pro/ko/opencv-mich-flaskleul-sayonghayeo-web-beulaujeoeseo-bidio-seuteuliming-162330575306240) | [깃허브](https://github.com/NakulLakhotia/Live-Streaming-using-OpenCV-Flask)
    * [Flask streaming Pedestrians detection using python opencv
](https://youtu.be/MAjbzx2zq-c) | [깃허브](https://github.com/seraj94ai/Flask-streaming-Pedestrians-detection-using-python-opencv-)
    * [Python OpenCV 영상 웹스트리밍 서버(Windows 용)](http://wandlab.com/blog/?p=94)

3. 통신
    * [스트리밍 서버를 이용한 AWS 기반의 딥러닝 플랫폼 구현과 성능
비교 실험](https://www.koreascience.or.kr/article/JAKO201908662571033.pdf)
    * [Socket.io 이용해서 python 프로그램끼리 영상 스트리밍](https://sungw.tistory.com/6)

---

### 📆 10월 목표
> * [플라스크 웹사이트 클론코딩](https://www.youtube.com/playlist?list=PLqIc89sXpwUBmr0Z282fm9JurDDYBE55r) 강의를 모두 수강하는 것이 목표
> * 기본 Flask 문법 및 예제 풀이, Flask Web Server의 개념과 작동 방식 숙지
> * API 사용 방법 익히기
> * 라즈베리 파이가 아직 없기 때문에 실습보다는 이론 위주로 공부해야할 것
> * 잠정적인 계획이므로 목표가 늘어날 수도, 줄어들 수도 있음

### 🤗 10월 Achievement 
> * 고라니 사진을 구글에서 크롤링하는 코드를 완성했다. 하지만 고라니가 우리나라를 제외한 국가에서는 희귀종이어서 사진을 찾기 힘들다. 고라니 검색을 하니 [이런 고라니](https://news.mt.co.kr/mtview.php?no=2021040714584548150) 사진도 뜬다. 심하면 일일이 수집해야 할 수도 있다..
> * AI Hub에서 데이터를 받았다. 사진이 100GB인데... 언제 날 잡아서 골라내야 할 것 같다.
> * [플라스크 웹사이트 클론코딩](https://www.youtube.com/playlist?list=PLqIc89sXpwUBmr0Z282fm9JurDDYBE55r) 강의를 모두 수강했다. 현재 [Do it! 점프 투 플라스크](https://wikidocs.net/book/4542)로 공부하는 중.
