Flutter와 Flask 연동하여 JSON 데이터 읽어오기
===
>*reference: https://www.youtube.com/watch?v=G000BuC_Ufs*

`http get`을 이용하여 제가 직접 만든 자체 서버 flask의 데이터를 가져오는 방법에 대한 예시 코드입니다.

***
### 1.
먼저 필요한 라이브러리/모듈을 임포트합니다.
```dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
```

다음은 메인 함수입니다. MyApp 클래스를 실행합니다.
```dart
/* main 함수 */
void main() {
  runApp(MyApp());
}
```

### 2. 
```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter to Python',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: HomePage(),
    );
  }
}
```
위는 MyApp 클래스에 대한 코드입니다. `StatelessWidget`, `build`, `BuildContext` 등 생소한 메소드들이 많이 나옵니다. 먼저 플러터를 이해하려면 위젯 개념을 이해해야 합니다.
> ### Widget
> * 플러터에서 위젯은 UI를 구성하는 모든 기본 단위요소이다. 
> * UI를 위젯에서 빌드한다. 
> * 위젯은 현재 설정과 상태에 따라 표현된다. 
> * 해당 위젯의 상태가 변경되면 위젯은 자동으로 재빌드된다.
> * 위젯의 종류로는 `StatelessWidget`, `StatefulWidget`, `InheritedWidget`이 있다. 여기서 대표적인 `StatelessWidget`과 `StatefulWidget`을 살펴본다.

> ### StatelessWidget
> * 상태가 없는 위젯이다. 따라서 변경될 필요가 없다.
> * 화면상에 존재하지만 실시간 데이터를 저장하지 않고 어떠한 상태도 가지지 않는다.

> ### StatefulWidget
> * 상태를 가지는 위젯이다. 사용자의 행동이나 데이터에 따라 모양이나 값이 바뀌는 위젯이다.

> ### Widget Tree
> * 위젯들은 트리 구조를 형성하면 정리된다. 한 위젯 안에 다른 위젯이 포함되는 부모 자식 관계로 저장하는 것이다. 부모 위젯을 위젯 컨테이너라고도 한다.
> * 이 위젯트리의 최상위에는 나의 프로젝트 이름이 존재한다. (MyApp)
> * `Scaffold 위젯`: 앱의 디자인과 기능을 구현하기 위한 빈 페이지를 제공하는 위젯. 이 위젯의 하위에 TExt나 Button 등의 위젯이 들어간다. 
> * 이 하위에는 `AppBar`나 `Text`나 눈에 보이고 보이지 않느 ㄴ모든 위젯들이 포함된다.
> * `Column 위젯`: 위젯을 세로로 위치시키기 위한 위젯.    

위젯의 구성은 아래와 같다.    

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fq10ql%2FbtqXD4EZyd2%2FPg5SBgmXM5qG0UzVCy1sJk%2Fimg.png)    

build: SLW, SFW에서 구현되며 화면을 구성할 UI들을 구현하는 메소드.
화면이 출력될 때 build 메소드가 호출되면서 build 메소드 내부에 구현한 UI 위젯들이 화면에 출력된다.


> ### build
> * 코드를 확인하면 build 메소드는 위젯을 리턴한다.
> * SLW, SFW에서 구현되며 화면을 구성할 UI들을 구현하는 메소드다.
> * 화면이 출력될 때 build 메소드가 호출되면서 build 메소드 내부에 구현한 UI 위젯들이 화면에 출력된다.

> ### BuildContext
> * BuildContext는 위젯 트리에서 현재 위젯의 위치를 알 수 있는 정보다.
> * BuildContext는 Stateless 위젯이나 state 빌드 메소드에 의해서 반환된 위젯의 부모가 된다.


### 3. 
```dart
class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}
```
> ### createState()
> * State 객체를 생성하는 역할
> * StatefulWidget 객체를 생성하면 생성자가 호출된다. 그 후 곧바로 createState()가 호출된다.
> * StatefuleWidget에서 필수적으로 오버라이드 해야하는 함수이다.

### 4.
```dart
class _HomePageState extends State<HomePage> {
  String greetings = '(Before)';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Container(
            child: Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        Text(greetings,
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
        Center(
            child: Container(
                width: 150,
                height: 60,
                child: TextButton(
                    onPressed: () async {
                      final response =
                          // 서버와 통신
                          await http.get(Uri.parse('http://10.0.2.2:5000/'));
                      final decoded =
                          json.decode(response.body) as Map<String, dynamic>;

                      setState(() {
                        greetings = decoded['greetings'];
                      });
                    },
                    child: Text(
                      'Press',
                      style: TextStyle(
                        fontSize: 24,
                        color: Colors.black,
                      ),
                    ))))
      ],
    )));
  }
}
```
> ### Text
> * Text는 말 그래도 Text

> ### Center
> * 일단 가운데 정렬


### 4. Server
```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET'])
def index():
    return jsonify({'greetings' : "안녕하세요, 저는 국희진입니다."})

if __name__ == '__main__':
    app.run(debug=True)
```
