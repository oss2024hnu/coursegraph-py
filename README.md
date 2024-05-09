# coursegraph-py
과목 이수체계도를 그려주는 프로그램을 오픈소스SW개발 수강생 모두가 함께 참여하며 개발하는 프로젝트입니다.

## 어떤 걸 해야하는가
1. ~ 이런 기능이 추가되면 좋겠다 혹은 현재 코드나 데이터에 어떤 문제점이 확인된다 등의 주제로 issue 만들기 - 2점
1. 현재 코드에서 ~ 이런 문제가 있어서 ~~ 이렇게 고쳤다는 pull request 올리기 - 3점
   
## 명령줄에서 실행법
1. Python과 git이 없다면 설치
1. 깃허브에서 coursegraph-py를 fork한 후 clone(복제), 아래 사이트 참고
    - https://m.blog.naver.com/3tpepper/222268448702
1. 현재 위치가 coursegraph-py가 아니라면 cd 명령어를 사용해 coursegraph-py 디렉터리로 이동
1. 파일을 실행할 때는 `python [파일명]` 으로 실행, ex) `python concept-demo.py` 또는 `python coursegraph` 또는 `python coursegraph/show_yaml.py`
1. `No module named`과 같은 에러 발생 시 "pip install [모듈이름]"으로 모듈 설치 (항상 이렇게 성공하진 않음. 모듈 이름과 패키지 이름이 다른 경우가 있기 때문)
1. 파일 수정은 각자가 편리하게 활용하는 코드 에디터를 활용


## 새로 참여하는 분들을 위한 정보 및 주의사항
onboarding 디렉토리의 문서들을 참고해 주세요

지금 아래 내용도 onboarding 디렉토리로 옴기는중

- 디렉토리 파일 경로를 처음에는 개발 편의를 위해 하드코딩으로 되어있는 경우도 남아있는데, 하드코딩 쓰지 않기
- coursegraph-py 프로젝트에서 입력 yaml 파일에 뭘 추가하자는 이슈는 더 이상 받지 않습니다
- `git add .` 절대 쓰지 않기!!
  구체적으로 어떤 파일을 새로 git이 관리하는 목록에 추가할지는 직접 하나하나 정해 주어야 합니다.
  왜냐하면 프로젝트를 하다 보면 저장소에 꼭 남겨놓아야 하는 소스코드와 입력파일 뿐 아니라
  프로그램 실행 과정에서 부가적으로 생기지만 저장소에 저장해 놓을 필요가 없는 임시 파일이나 로그 파일 등등 부수적인 파일들도 생기는데 
  현재 디렉토리에 있는거 전부 다 추가하라는 `git add .` 같은 명령을 내리면 추가해서는 안되는 파일까지 저장소에 추가됩니다.
  하나하나 파일 입력하는 게 귀찮으면 쉘에서 지원되는 탭 자동완성 기능을 활용하던가 아니면 vscode 등에서 지원하는 GUI를 통해서 git 관련 작업을 하면 됩니다.
- gui 같은 부가 작업은 main 함수가 아닌 gui함수에 따로 작업해주시면 됩니다. main함수에는 최소한의 기능만 남겨야 합니다.

## `cousergraph/__main__.py` 사용방법
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
  `-f` 혹은 `--foramt` 옵션을 제공하지 한은 경우도 graph 모드로 동작. 아직 CLI 인터페이스와 실제 동작하는 코드가 연결되어 있지 않음. 연결해서 테스트 해봐야. 
- `-f table` 혹은 `--format table` 옵션을 주었을 경우,
  현재는 인터페이스 일관성이 좀 떨어지는 상태라 실행하면 파일을 입력하라고 나오는데, 예를 들어서 me.yaml파일을 출력하고 싶으면 표준입력에 me만 입력하면 me.yaml 파일의 표가 나온다.
  이거는 앞으로 개선해야 하는 사항이다. 지금 이거를 표준입력을 받는 게 아니라 `--input` 옵션으로 받도록 통일해야 함. 출력되는 이미지도 `--output` 옵션으로 받도록 좀 통일하고.


## 참고사항
- pr과 이슈를 연결하는 법 github docs 링크: https://docs.github.com/ko/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
