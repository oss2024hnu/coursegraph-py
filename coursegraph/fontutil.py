# 한글 폰트 정보를 가져오는 모듈
# 제발 ttf 파일 path를 하드코딩하지 말 것!!!
import os
import platform
def get_system_font(): # 시스템 확인 후 폰트 지정 함수
    system = platform.system()
    if system == 'Windows':
        # Windows의 경우, 시스템 폰트 경로로 설정
        font_folder = os.environ.get("SystemRoot", "C:\\Windows") + "\\Fonts\\malgun.ttf"
        return [font_folder]
    elif system == 'Darwin':
        # macOS의 경우, 기본 시스템 폰트 경로 설정 (MacOS 애플고딕의 정확한 이름 표기가 필요함)
        return ['/System/Library/Fonts/AppleGothic.ttf']
    elif system == 'Linux':
        font_folder = os.environ.get("FONTCONFIG_PATH")
        # 환경 변수 값이 None이면 기본 경로 사용
        if font_folder is None:
            font_folder = "/usr/share/fonts/"
        font_folder = os.path.join(font_folder, "DejaVu_Sans.ttf")  # 한글을 지원하는 DejaVu_Sans 폰트로 설정하였습니다.
        return [font_folder]
    else:
        # 기타 운영 체제의 경우, 적절한 시스템 폰트 경로를 설정해야 합니다. (현재 리눅스의 파일 경로에 맞춰 설정되어있음) ===> 리눅스에 맞지 않음!! 배포판마다 위치 다름 이런 하드코딩 정말 안좋습니다
        # return ['/usr/share/fonts/truetype/NanumGothic.ttf']
        return None
