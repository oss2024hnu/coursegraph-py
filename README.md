# coursegraph-py
과목 이수체계도를 그려주는 프로그램을 오픈소스SW개발 수강생 모두가 함께 참여하며 개발하는 프로젝트입니다.

## 새로 참여하는 분들을 위한 정보 및 주의사항
onboarding 디렉토리의 문서들을 참고해 주세요


### 개발환경 설치 및 최초로 실행해 보는 법 <=== 이것도 onboarding 디렉토리로 옮길 내용에 포함됩니다
1. Python과 git이 없다면 설치
1. 깃허브에서 coursegraph-py를 fork한 후 clone(복제), 아래 사이트 참고
    - https://m.blog.naver.com/3tpepper/222268448702
1. 현재 위치가 coursegraph-py가 아니라면 cd 명령어를 사용해 coursegraph-py 디렉터리로 이동
1. 파일을 실행할 때는 `python [파일명]` 으로 실행, ex) `python coursegraph` 또는 `python coursegraph/__main__.py`
1. `pip install -r requirements.txt`를 실행하면 필요한 모듈들이 모두 설치되도록 requirements.txt를 작성하고 있으나
   개발 도중에 추가되는 기능에 필요한 모듈이 혹시 모자라서 `No module named`과 같은 에러 발생 시
   "pip install [모듈이름]"으로 모듈 설치 (항상 이렇게 성공하진 않음. 모듈 이름과 패키지 이름이 다른 경우가 있기 때문)
1. 파일 수정은 각자가 편리하게 활용하는 코드 에디터를 활용

## 프로그램 사용법

## CLI 사용법
다음과 같이 `cousergraph/__main__.py`를 파이썬으로 실행시켜 활용한다.
```
oss2024hnu/coursegraph-py$ python coursegraph --help
usage: coursegraph [-h] [-i INPUT] [-o OUTPUT] [-v] [-f {graph,table}]

A CLI utility for processing data.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Specify the input YAML data file path. (required)
  -o OUTPUT, --output OUTPUT
                        Specify the output image file path. (optional)
  -v, --verbose         Enable verbose mode.
  -f {graph,table}, --format {graph,table}
                        Sepcify the output format (graph, table). Defaults to graph.

Enjoy using the CLI utility!
```
- `-i` 혹은 `--input` 옵션에는 반드시 입력 데이터인 YAML 파일을 필수로 제공해야 함
- `-o` 혹은 `--output` 옵션에는 생성할 이미지 파일의 이름을 제공하여 이미지를 생성하도록 할 수 있는데, 제공하지 않는 경우 팝업 다이얼로그 창으로 이미지를 띄워서 보여주려고 할 것임 (다만 그래픽을 지원하지 않는 환경에서는 작동하지 않음).
- `-f graph` 혹은 `--format graph` 옵션을 제공하면 이수체계도를 방향그래프 형태로 보여줌.
  `-f` 혹은 `--foramt` 옵션을 제공하지 않은 경우도 graph 모드로 동작.
- `-f table` 혹은 `--format table` 옵션을 주었을 경우, yaml 파일의 전체 내용을 한꺼번에 보기 좋은 표의 형태로 보여준다.

### GUI 사용법 <=== 아직 여기에 대한 문서가 프로젝트 내에 없느 거 같네요 이것도 이슈로 만들어서 진행해볼 만한 거리입니다
TODO

## 참고사항
- pr과 이슈를 연결하는 법 github docs 링크: https://docs.github.com/ko/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
