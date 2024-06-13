### 개발환경 설치 및 최초로 실행해 보는 법
1. Python과 git 그리고 make가 없다면 설치 (make 설치법은 이 문서와 같은 디렉토리의 TestPR 문서 참고)
1. 깃허브에서 coursegraph-py를 fork한 후 clone(복제), 아래 사이트 참고
    - https://m.blog.naver.com/3tpepper/222268448702
1. 현재 위치가 coursegraph-py가 아니라면 cd 명령어를 사용해 coursegraph-py 디렉터리로 이동
1. 파일을 실행할 때는 `python [파일명]` 으로 실행, ex) `python coursegraph` 또는 `python coursegraph/__main__.py`
1. `pip install -r requirements.txt`를 실행하면 필요한 모듈들이 모두 설치되도록 requirements.txt를 작성하고 있으나
   개발 도중에 추가되는 기능에 필요한 모듈이 혹시 모자라서 `No module named`과 같은 에러 발생 시
   "pip install [모듈이름]"으로 모듈 설치 (항상 이렇게 성공하진 않음. 모듈 이름과 패키지 이름이 다른 경우가 있기 때문)
1. 파일 수정은 각자가 편리하게 활용하는 코드 에디터를 활용
