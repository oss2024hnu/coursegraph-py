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
1. 파일을 실행할 때는 `python [파일명]` 으로 실행, ex) `python concept-demo.py` 또는 python __main__.py
1. `No module named`과 같은 에러 발생 시 "pip install [모듈이름]"으로 모듈 설치 (항상 이렇게 성공하진 않음. 모듈 이름과 패키지 이름이 다른 경우가 있기 때문)
1. 파일 수정은 각자가 편리하게 활용하는 코드 에디터를 활용


## 주의사항
- issue 등록 시 꼭 중복된게 있는지 확인 후 등록. 현재 open된 이슈 뿐만 아니라 이미 closed된 이슈서 논의된 것도 있을 수 있음
- requests시 잘 돌아가는지 테스트 후 등록
- 전에는 ai-concept-demo에서 수정했지만, 앞으로는 coursegraph 안에 내용을 수정 (ai-concept-demo를 pull requests할 시 점수 안줌)
- 디렉토리 파일 경로를 처음에는 개발 편의를 위해 하드코딩으로 되어있는 경우도 남아있는데, 하드코딩 쓰지 않기
- issues : pull requests = 4 : 1 비율로 등록하기
- coursegraph-py 프로젝트에서 입력 yaml 파일에 뭘 추가하자는 이슈는 더 이상 받지 않습니다
- "gii add .에 대한 주의 사항"
구체적으로 어떤 파일을 새로 git이 관리하는 목록에 추가할지는 직접 하나하나 정해 주어야 합니다.
왜냐하면 프로젝트를 하다 보면 저장소에 꼭 남겨놓아야 하는 소스코드와 입력파일 뿐 아니라
프로그램 실행 과정에서 부가적으로 생기지만 저장소에 저장해 놓을 필요가 없는 임시 파일이나 로그 파일 등등 부수적인 파일들도 생기는데 
현재 디렉토리에 있는거 전부 다 추가하라는 git add . 같은 명령을 내리면 추가해서는 안되는 파일까지 저장소에 추가됩니다.
하나하나 파일 입력하는 게 귀찮으면 쉘에서 지원되는 탭 자동완성 기능을 활용하던가 아니면 vscode 등에서 지원하는 GUI를 통해서 git 관련 작업을 하면 됩니다.

## main.py사용방법
- -i 명령어 사용 방법
```
python coursegraph -i [입력할 파일 주소]
```
- -o 명령어 사용 방법
```
python coursegraph -o [출력할 파일 주소]
```
- -s 명령어 사용방법
```
python coursegraph -s 입력
```
파일을 입력하라고 나오는데 예를 들어서 me.yaml파일을 출력하고 싶으면 me만 입력하면 me.yaml 파일의 표가 나온다


## 참고사항
- pr과 이슈를 연결하는 법 github docs 링크: https://docs.github.com/ko/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
