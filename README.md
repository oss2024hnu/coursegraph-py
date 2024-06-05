# coursegraph-py
과목 이수체계도를 그려주는 프로그램을 오픈소스SW개발 수강생 모두가 함께 참여하며 개발하는 프로젝트입니다.

## 새로 참여하는 분들을 위한 정보 및 주의사항
onboarding 디렉토리의 문서들을 참고해 주세요

## 프로그램 사용법

## 한글 설치 방법
1. Codespace를 실행한 뒤 터미널에 './install_fonts.sh' 실행
2. 실행 완료 후 실행했던 Codespace의 중지 후 재부팅 <== 이거는 안해도 되는데 혹시 안될때 해보라는 겁니다.
   1) 중지하려는 Codespace의 오른쪽에 있는 줄임표(...)를 클릭
   2) Codespace 중지를 클릭
   3) Codespace를 다시 재시작
3. Codespace 실행 후 정상적으로 작동하는지 확인
    'python coursegraph -i data/input.yaml -o out.png' 명령어 실행

### CLI 사용법
다음과 같이 `cousergraph/__main__.py`를 파이썬으로 실행시켜 활용한다.
```
oss2024hnu/coursegraph-py$ python coursegraph --help
usage: coursegraph [-h] [-o OUTPUT] [-f {graph,table}] [-s SIZE] input

A CLI utility for processing data.

positional arguments:
  input                 Specify the input YAML data file path. (required)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Specify the output image file path. (optional)
  -v, --verbose         Enable verbose mode.
  -f {graph,table}, --format {graph,table}
                        Sepcify the output format (graph, table). Defaults to graph.
  -s WIDTH,HEIGHT , --size WIDTH,HEIGHT 
                        Specify the size of the output image in format WIDTH x HEIGHT(optional)

Enjoy using the CLI utility!
```
- `-o` 혹은 `--output` 옵션에는 생성할 이미지 파일의 이름을 제공하여 이미지를 생성하도록 할 수 있는데, 제공하지 않는 경우 팝업 다이얼로그 창으로 이미지를 띄워서 보여주려고 할 것임 (다만 그래픽을 지원하지 않는 환경에서는 작동하지 않음).
- `-f graph` 혹은 `--format graph` 옵션을 제공하면 이수체계도를 방향그래프 형태로 보여줌.
  `-f` 혹은 `--foramt` 옵션을 제공하지 않은 경우도 graph 모드로 동작.
- `-f table` 혹은 `--format table` 옵션을 주었을 경우, yaml 파일의 전체 내용을 한꺼번에 보기 좋은 표의 형태로 보여준다.
- '-s WIDTH,HEIGHT' 혹은 '--size WIDTH,HEIGHT' 옵션을 제공했을 경우 이미지의 크기를 가로,세로의 입력값으로 지정해준다.
  '-s' 혹은 '--size' 옵션을 제공하지 않은 경우에는 이미지의 크기는 10,20 으로 지정된다. 

### GUI 사용법
coursegraph-py/coursegraph로 이동한 다음 'python gui.py'를 터미널에 넣고 실행하면 gui화면이 나온다.
현재 사용가능한 기능은 파일 열기, 다른이름으로 저장하기, 연 이미지를 초기화 시키는 기능이 있다.
파일 열기와 다른 이름으로 저장하기는 오른쪽위에 있는 파일을 클릭하면 기능을 사용할 수 있다.
이미지를 초기화하는 기능은 아래에 이미지 초기화 버튼이 있는데 클릭하면 이미지가 초기화됩니다.
gui파일에 대해서 사람들의 생각이 다르기 때문에 어떤 기능이나 내용을 추가할지 온보딩에 그림을 이용해서 의견을 공유하면 어떤 내용이 필요한지 보기 편할 것 같습니다.

PyQt5 desiner 사용법

-  Windows (터미널)
- pip install pyqt5
- pip install pyqt5-tools
- 이후 본인 python 설치 폴더 내부 \Lib\site-packages\qt5_applications\Qt\bin 내부에 있는 desiner 실행

- MacOS (터미널 OR VScode)
- pip install pyqt
- pip install pyqt5-tools
- 이후 본인 python 설치 폴더 내부 \Lib\site-packages\qt5_applications\Qt\bin 내부에 있는 desiner 실행

- 데비안 계열(우분투 등) Linux (터미널)
- `pip3 install pyqt5`  (시스템에 따라서는 pip3가 아니라 pip로 실행해도 되는 경우도 있음)
- `sudo apt install python3-pyqt5`
- `sudo apt install pyqt5-dev-tools`
- `sudo apt install qttools5-dev-tools`
- 이후 터미널에서 `desiner` 로 실행

## 참고사항
- pr과 이슈를 연결하는 법 github docs 링크: https://docs.github.com/ko/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
